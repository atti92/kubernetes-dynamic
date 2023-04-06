# Copyright 2019 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations

import re
from typing import TYPE_CHECKING, Callable, Generic, Iterator, Optional, Type, TypeVar, cast, overload

from kubernetes_dynamic.events import Event, Watch
from kubernetes_dynamic.exceptions import EventTimeoutError
from kubernetes_dynamic.formatters import format_selector
from kubernetes_dynamic.kube.exceptions import ConflictError, NotFoundError, UnprocessibleEntityError
from kubernetes_dynamic.models.resource_value import ResourceValue

R = TypeVar("R", bound=ResourceValue)

if TYPE_CHECKING:
    from kubernetes_dynamic.client import K8sClient
    from kubernetes_dynamic.models.common import ItemList
    from kubernetes_dynamic.models.resource_item import CheckResult


class _Missing:
    pass


MISSING = _Missing()


class ResourceApi(Generic[R]):
    """Represents an API resource type, containing the information required to build urls for requests"""

    def __init__(
        self,
        prefix=None,
        group=None,
        api_version=None,
        kind=None,
        namespaced=False,
        verbs=None,
        name=None,
        preferred=False,
        client=None,
        singularName=None,
        shortNames=None,
        categories=None,
        subresources=None,
        resource_type=None,
        **kwargs,
    ):

        if None in (api_version, kind, prefix):
            raise ValueError("At least prefix, kind, and api_version must be provided")

        self.prefix = prefix
        self.group = group
        self.api_version = api_version
        self.kind = kind
        self.namespaced = namespaced
        self.verbs = verbs
        self.name = name
        self.preferred = preferred
        self.singular_name = singularName or (name[:-1] if name else "")
        self.short_names = shortNames
        self.categories = categories
        self.subresources = {k: Subresource(self, **v) for k, v in (subresources or {}).items()}
        self.client: K8sClient = client
        self.resource_type: Optional[Type[R]] = resource_type

        self.extra_args = kwargs

    def to_dict(self):
        d = {
            "_type": "Resource",
            "prefix": self.prefix,
            "group": self.group,
            "api_version": self.api_version,
            "kind": self.kind,
            "namespaced": self.namespaced,
            "verbs": self.verbs,
            "name": self.name,
            "preferred": self.preferred,
            "singularName": self.singular_name,
            "shortNames": self.short_names,
            "categories": self.categories,
            "subresources": {k: sr.to_dict() for k, sr in self.subresources.items()},
        }
        d.update(self.extra_args)
        return d

    @property
    def group_version(self) -> str:
        if self.group:
            return "{}/{}".format(self.group, self.api_version)
        return cast(str, self.api_version)

    def __repr__(self):
        return "<{}({}/{})>".format(self.__class__.__name__, self.group_version, self.name)

    @property
    def urls(self) -> dict[str, str]:
        full_prefix = "{}/{}".format(self.prefix, self.group_version)
        resource_name = self.name.lower()
        return {
            "base": "/{}/{}".format(full_prefix, resource_name),
            "namespaced_base": "/{}/namespaces/{{namespace}}/{}".format(full_prefix, resource_name),
            "full": "/{}/{}/{{name}}".format(full_prefix, resource_name),
            "namespaced_full": "/{}/namespaces/{{namespace}}/{}/{{name}}".format(full_prefix, resource_name),
        }

    def path(self, name=None, namespace=None) -> str:
        url_type = []
        path_params = {}
        if self.namespaced and namespace:
            url_type.append("namespaced")
            path_params["namespace"] = namespace
        if name:
            url_type.append("full")
            path_params["name"] = name
        else:
            url_type.append("base")
        return self.urls["_".join(url_type)].format(**path_params)

    def __getattr__(self, name) -> Subresource:
        if name in self.subresources:
            return self.subresources[name]
        raise AttributeError(name)

    def serialize_body(self, body):
        """Serialize body to raw dict so apiserver can handle it

        :param body: kubernetes resource body, current support: Union[Dict, ResourceValue]
        """
        if callable(getattr(body, "to_dict", None)):
            return body.to_dict()
        return body or {}

    def ensure_namespace_param(self, namespace: Optional[str | _Missing], body=None, allow_all=False) -> Optional[str]:
        if not self.namespaced:
            return None
        if namespace is MISSING:
            if body:
                namespace = body.get("metadata", {}).get("namespace", self.config.namespace)
            else:
                namespace = self.client.config.namespace
        if not allow_all and not namespace:
            raise ValueError("Namespace is required for {}.{}".format(self.group_version, self.kind))
        return cast(Optional[str], namespace)

    def ensure_name_param(self, name, body=None) -> str:
        if not name and body:
            name = body.get("metadata", {}).get("name")
        if not name:
            raise ValueError("Name is required for {}.{}".format(self.group_version, self.kind))
        return name

    @overload
    def read(
        self,
        *,
        namespace: Optional[str | _Missing] = None,
        label_selector: Optional[str] = None,
        field_selector: Optional[str] = None,
        **kwargs,
    ) -> ItemList[R]:
        """Get a list of models.
        Setting namespace to `None` or `""` will yield from all namespaces.

        Args:
            namespace: namespace of the resource. Defaults to `current` set to None/Empty for all.
            label_selector: Label selectors to use for query.
            field_selector: Field selectors to use for query.
        """
        ...  # pragma: no cover

    @overload
    def read(self, name: str, namespace: Optional[str | _Missing] = None, **kwargs) -> R:
        """Get a resource model.

        Args:
            name: name of the resource you want to query.
            namespace: namespace of the resource. Defaults to `current`.

        Raises:
            NotFoundError: When the model does not exists.
        """
        ...  # pragma: no cover

    def read(
        self, name: Optional[str] = None, namespace: Optional[str | _Missing] = MISSING, **kwargs
    ) -> R | ItemList[R]:
        namespace = self.ensure_namespace_param(namespace, allow_all=not name)
        path = self.path(name=name, namespace=namespace)
        return self.client.request("get", path, **kwargs)

    @overload
    def get(
        self,
        *,
        namespace: Optional[str | _Missing] = MISSING,
        label_selector: Optional[str] = None,
        field_selector: Optional[str] = None,
        **kwargs,
    ) -> ItemList[R]:
        """Get a list of models.
        Setting namespace to `None` or `""` will yield from all namespaces.

        Args:
            namespace: namespace of the resource. Defaults to `current` set to None/Empty for all.
            label_selector: Label selectors to use for query.
            field_selector: Field selectors to use for query.
        """
        ...  # pragma: no cover

    @overload
    def get(self, name: str, namespace: Optional[str | _Missing] = MISSING, **kwargs) -> Optional[R]:
        """Get a resource model.

        Args:
            name: name of the resource you want to query.
            namespace: namespace of the resource. Defaults to `current`.
        """
        ...  # pragma: no cover

    def get(
        self, name: Optional[str] = None, namespace: Optional[str | _Missing] = MISSING, **kwargs
    ) -> Optional[R] | ItemList[R]:
        try:
            return self.read(name, namespace, **kwargs) if name else self.read(namespace=namespace, **kwargs)
        except NotFoundError:
            return None

    def find(self, pattern: str, namespace: Optional[str | _Missing] = MISSING, **kwargs) -> list[R]:
        """Find a list of models.
        Setting namespace to `None` or `""` will yield from all namespaces.

        Args:
            pattern: regex pattern for metadata.name.
            namespace: namespace of the resource. Defaults to `current` set to None/Empty for all.
            label_selector: Label selectors to use for query.
            field_selector: Field selectors to use for query.
        """
        items = []
        data: Optional[ItemList[R]] = self.get(namespace=namespace, **kwargs)
        if not data:
            return items
        for item in data:
            if re.match(pattern, item.metadata.name):
                items.append(item)
        return items

    def create(self, body: dict | R, namespace: Optional[str | _Missing] = MISSING, **kwargs) -> R:
        body = self.serialize_body(body)
        namespace = self.ensure_namespace_param(namespace, body)
        path = self.path(namespace=namespace)
        return self.client.request("post", path, body=body, **kwargs)

    @overload
    def delete(
        self, name: str, namespace: Optional[str | _Missing] = MISSING, body: Optional[dict | R] = None, **kwargs
    ) -> R:
        ...  # pragma: no cover

    @overload
    def delete(
        self,
        *,
        namespace: Optional[str | _Missing] = MISSING,
        body: Optional[dict | R] = None,
        label_selector: Optional[str] = None,
        field_selector: Optional[str] = None,
        **kwargs,
    ) -> ItemList[R]:
        ...  # pragma: no cover

    def delete(
        self,
        name: Optional[str] = None,
        namespace: Optional[str | _Missing] = MISSING,
        body: Optional[dict | R] = None,
        label_selector: Optional[str] = None,
        field_selector: Optional[str] = None,
        **kwargs,
    ) -> ItemList[R] | R:
        if not (name or label_selector or field_selector):
            raise ValueError("At least one of name|label_selector|field_selector is required")
        if self.namespaced and not (label_selector or field_selector):
            namespace = self.ensure_namespace_param(namespace, allow_all=not name)
        path = self.path(name=name, namespace=namespace)
        return self.client.request(
            "delete", path, body=body, label_selector=label_selector, field_selector=field_selector, **kwargs
        )

    def replace(
        self, body: dict | R, name: Optional[str] = None, namespace: Optional[str | _Missing] = MISSING, **kwargs
    ) -> R:
        body = self.serialize_body(body)
        name = self.ensure_name_param(name, body)
        namespace = self.ensure_namespace_param(namespace, body)
        path = self.path(name=name, namespace=namespace)
        return self.client.request("put", path, body=body, **kwargs)

    def patch(
        self, body: dict | R, name: Optional[str] = None, namespace: Optional[str | _Missing] = MISSING, **kwargs
    ) -> R:
        body = self.serialize_body(body)
        name = self.ensure_name_param(name, body)
        namespace = self.ensure_namespace_param(namespace, body)

        content_type = kwargs.pop("content_type", "application/strategic-merge-patch+json")
        path = self.path(name=name, namespace=namespace)

        return self.client.request("patch", path, body=body, content_type=content_type, **kwargs)

    def server_side_apply(
        self,
        body: dict | R,
        name: Optional[str] = None,
        namespace: Optional[str | _Missing] = MISSING,
        force_conflicts: Optional[bool] = None,
        **kwargs,
    ) -> R:
        body = self.serialize_body(body)
        name = self.ensure_name_param(name, body)
        namespace = self.ensure_namespace_param(namespace, body)

        kwargs.update({"content_type": "application/apply-patch+yaml"})
        path = self.path(name=name, namespace=namespace)

        return self.client.request("patch", path, body=body, force_conflicts=force_conflicts, **kwargs)

    def watch(
        self,
        namespace: Optional[str | _Missing] = MISSING,
        name: Optional[str] = None,
        label_selector: Optional[str] = None,
        field_selector: Optional[str] = None,
        resource_version: Optional[str] = None,
        timeout: Optional[float] = None,
        watcher: Optional[Watch] = None,
    ) -> Iterator[Event[R]]:
        namespace = self.ensure_namespace_param(namespace, allow_all=True)
        if name:
            field_selector = field_selector or ""
            field_selector += f",metadata.name={name}"
        watcher = watcher or Watch(self.client.client, self.resource_type)
        if watcher and not resource_version:
            resource_version = watcher.resource_version
        return watcher.stream(
            self.get,
            namespace=namespace or self.client.config.namespace,
            name=None,
            field_selector=field_selector,
            label_selector=label_selector,
            resource_version=resource_version,
            serialize=False,
            timeout_seconds=timeout,
        )

    def wait_until(
        self,
        *,
        namespace: Optional[str | _Missing] = MISSING,
        name: Optional[str] = None,
        check: Callable[[Event], CheckResult],
        field_selector: Optional[str] = None,
        label_selector: Optional[str] = None,
        timeout: int = 30,
        **kwargs,
    ) -> Event:
        """Wait until a certain custom check returns true for a resource returned by the stream."""
        namespace = self.ensure_namespace_param(namespace)
        field_selectors = [] if not field_selector else [format_selector(field_selector)]
        if name:
            field_selectors.append(f"metadata.name={name}")

        last = None
        result = None
        for event in self.watch(
            field_selector=format_selector(field_selectors),
            label_selector=format_selector(label_selector),
            timeout=timeout,
            namespace=namespace,
            **kwargs,
        ):
            last = event
            result = check(event)
            if result:
                return event
        if last is None:
            raise EventTimeoutError(f"Timed out waiting for check. {self.kind} {name} not found.", last=last)
        if result is not None and result.message:
            raise EventTimeoutError(result.message, last=last)
        raise EventTimeoutError(f"Timed out waiting for check on {self.kind} {name} .", last=last)

    def apply(self, body: dict | R, namespace: Optional[str | _Missing] = MISSING, **kwargs) -> R:
        namespace = self.ensure_namespace_param(namespace)
        body["metadata"].setdefault("annotations", {})
        name = body["metadata"]["name"]
        try:
            return self.create(body=body, namespace=namespace, **kwargs)
        except ConflictError:
            pass
        try:
            return self.patch(name=name, body=body, namespace=namespace, **kwargs)
        except UnprocessibleEntityError:
            pass

        self.delete(name=name, namespace=namespace, **kwargs)
        return self.create(body=body, namespace=namespace, **kwargs)


class ResourceList(ResourceApi):
    """Represents a list of API objects"""

    def __init__(self, client, group="", api_version="v1", base_kind="", kind=None, base_resource_lookup=None):
        self.client = client
        self.group = group
        self.api_version = api_version
        self.kind = kind or "{}List".format(base_kind)
        self.base_kind = base_kind
        self.base_resource_lookup = base_resource_lookup
        self.__base_resource = None

    def base_resource(self):
        if self.__base_resource:
            return self.__base_resource
        elif self.base_resource_lookup:
            self.__base_resource = self.client.resources.get(**self.base_resource_lookup)
            return self.__base_resource
        elif self.base_kind:
            self.__base_resource = self.client.resources.get(
                group=self.group, api_version=self.api_version, kind=self.base_kind
            )
            return self.__base_resource
        return None

    def _items_to_resources(self, body):
        """Takes a List body and return a dictionary with the following structure:
        {
            'api_version': str,
            'kind': str,
            'items': [{
                'resource': Resource,
                'name': str,
                'namespace': str,
            }]
        }
        """
        if body is None:
            raise ValueError("You must provide a body when calling methods on a ResourceList")

        api_version = body["apiVersion"]
        kind = body["kind"]
        items = body.get("items")
        if not items:
            raise ValueError("The `items` field in the body must be populated when calling methods on a ResourceList")

        if self.kind != kind:
            raise ValueError(
                "Methods on a {} must be called with a body containing the same kind. Receieved {} instead".format(
                    self.kind, kind
                )
            )

        return {"api_version": api_version, "kind": kind, "items": [self._item_to_resource(item) for item in items]}

    def _item_to_resource(self, item):
        metadata = item.get("metadata", {})
        resource = self.base_resource()
        if not resource:
            api_version = item.get("apiVersion", self.api_version)
            kind = item.get("kind", self.base_kind)
            resource = self.client.resources.get(api_version=api_version, kind=kind)
        return {
            "resource": resource,
            "definition": item,
            "name": metadata.get("name"),
            "namespace": metadata.get("namespace"),
        }

    def to_dict(self):
        return {
            "_type": "ResourceList",
            "group": self.group,
            "api_version": self.api_version,
            "kind": self.kind,
            "base_kind": self.base_kind,
        }

    def __getattr__(self, name):
        if self.base_resource():
            return getattr(self.base_resource(), name)
        return None


class Subresource(ResourceApi):
    """Represents a subresource of an API resource. This generally includes operations
    like scale, as well as status objects for an instantiated resource
    """

    def __init__(self, parent, **kwargs):
        self.parent = parent
        self.prefix = parent.prefix
        self.group = parent.group
        self.api_version = parent.api_version
        self.kind = kwargs.pop("kind")
        self.name = kwargs.pop("name")
        self.subresource = kwargs.pop("subresource", None) or self.name.split("/")[1]
        self.namespaced = kwargs.pop("namespaced", False)
        self.verbs = kwargs.pop("verbs", None)
        self.extra_args = kwargs

    @property
    def urls(self):
        full_prefix = "{}/{}".format(self.prefix, self.group_version)
        return {
            "full": "/{}/{}/{{name}}/{}".format(full_prefix, self.parent.name, self.subresource),
            "namespaced_full": "/{}/namespaces/{{namespace}}/{}/{{name}}/{}".format(
                full_prefix, self.parent.name, self.subresource
            ),
        }

    def to_dict(self):
        d = {
            "kind": self.kind,
            "name": self.name,
            "subresource": self.subresource,
            "namespaced": self.namespaced,
            "verbs": self.verbs,
        }
        d.update(self.extra_args)
        return d

    def __getattr__(self, name) -> Subresource:
        return getattr(self.parent, name)
