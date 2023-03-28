from __future__ import annotations

import re
import typing
from typing import Optional

import pydantic
from kubernetes import dynamic
from kubernetes.dynamic.exceptions import NotFoundError
from typing_extensions import Self

from .resource_api import ResourceApi
from .resource_field import ResourceValue

if typing.TYPE_CHECKING:
    from .client import K8sClient
    from .models import V1ObjectMeta


class CheckResult:
    """Result object to represent the result and message of a check."""

    def __init__(self, state: bool, message: Optional[str] = None) -> None:
        self.state = state
        self.message = message

    def __bool__(self):
        return bool(self.state)

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, CheckResult):
            return self.state == __o.state and self.message == __o.message
        return bool(self) == __o


class ResourceItem(ResourceValue):
    """Kubernetes resource objects."""

    apiVersion: str
    kind: str
    metadata: V1ObjectMeta
    status: ResourceValue

    _client: Optional[K8sClient] = pydantic.PrivateAttr()
    _api: Optional[ResourceApi] = pydantic.PrivateAttr()

    def __init__(
        self,
        definition: dict | dynamic.ResourceInstance | dynamic.ResourceField | None = None,
        client=None,
        **kwargs,
    ):
        final_def: dict = {}
        if isinstance(definition, dict):
            final_def = definition
        elif isinstance(definition, dynamic.ResourceField):
            final_def = definition.__dict__
        elif isinstance(definition, dynamic.ResourceInstance):
            final_def = definition.to_dict()  # type: ignore
            client = definition.client
        final_def.update(kwargs)
        final_def.setdefault("kind", self.kind)
        final_def.setdefault("apiVersion", self.apiVersion)
        if not final_def.get("kind") or not final_def.get("apiVersion"):
            for cl in [self.__class__] + list(self.__class__.__bases__):
                parts = re.sub("([a-z0-9])([A-Z])", r"\1 \2", cl.__name__).split()
                match = [part for part in parts if re.match(r"^V\d.*", part)]
                if match:
                    version = match[0]
                    version_index = parts.index(version) + 1
                    final_def.setdefault("kind", "".join(parts[version_index:]))
                    final_def.setdefault("apiVersion", version.lower())
                    break
        super().__init__(**final_def)

        self._api: Optional[ResourceApi] = None
        self._client = client

    @classmethod
    def serialize(cls, client, instance: dict, **kwargs) -> Self | list[Self]:
        """Serialize object from dictionary like objects."""
        kind = instance["kind"]
        if kind.endswith("List") and "items" in instance:
            items = []
            kind = instance["kind"][:-4]
            for item in instance["items"]:
                if "apiVersion" not in item:
                    item["apiVersion"] = instance["apiVersion"]
                if "kind" not in item:
                    item["kind"] = kind
                items.append(cls(item, client, **kwargs))
            return items
        return cls(instance, client, **kwargs)

    @property
    def api(self) -> ResourceApi:
        """Get resource api."""
        if not self._api or self._api.api_version != self.apiVersion or self._api.kind != self.kind:
            self._api = self.client.get_api(kind=self.kind, api_version=self.apiVersion)
        return self._api

    @property
    def client(self) -> K8sClient:
        """Get resource api."""
        if not self._client:
            self._client = self.default_client()
        return self._client

    @classmethod
    def default_client(cls) -> K8sClient:
        """Create a default K8sClient."""
        from .client import K8sClient

        return K8sClient()

    def refresh(self) -> Self:
        """Refreshes the local instance with kubernetes data."""
        data = self.read()
        if data is None:
            raise NotFoundError(self)
        return self._update_attrs(data)

    def patch(self) -> Self:
        """Updates the Kubernetes resource."""
        return self._update_attrs(self.api.patch(name=self.metadata.name, body=self))

    def create(self) -> Self:
        """Creates the object in Kubernetes."""
        return self._update_attrs(self.api.create(self))

    def read(self) -> Optional[Self]:
        """Reads the object in Kubernetes."""
        return self.api.get(self.metadata.name, self.metadata.namespace)

    def delete(self) -> Self:
        """Deletes the object from Kubernetes."""
        return self.api.delete(self.metadata.name, self.metadata.namespace)

    @staticmethod
    def check_object_conditions(item: ResourceItem) -> CheckResult:
        """Check object conditions."""
        name = item.metadata.name
        if not item.status or not item.status.conditions:
            return CheckResult(False, f"No conditions found on {item.kind} {name}.")
        for condition in item.status.conditions:
            if condition.status != "True":
                untrue_condition = condition
                break
        else:
            return CheckResult(True, f"All conditions true on {item.kind} {name}.")
        return CheckResult(False, f"Condition not true on {item.kind} {name} : {untrue_condition}.")

    @staticmethod
    def check_replicas_ready(item: ResourceItem) -> CheckResult:
        """Check object replicas."""
        item_dict = item.dict()
        replicas = item_dict["status"].get("replicas", 0)
        name = item.metadata.name
        ready_replicas = item.status.readyReplicas or 0
        if ready_replicas == replicas:
            return CheckResult(True, f"All {replicas} replicas ready on {item.kind} {name}.")
        else:
            return CheckResult(
                False,
                f"{item.kind} {name} only have {ready_replicas} ready " f"replicas out of required {replicas}.",
            )

    @staticmethod
    def check_object_is_ready(item: ResourceItem) -> CheckResult:
        """Checks whether given resource object is ready or not.

        For resources that control replicas it checks whether all replicas are ready, otherwise it
        checks whether all status conditions are true.
        """
        if not item.status:
            return CheckResult(False, "Object has no status description.")
        if item.status.replicas:
            return ResourceItem.check_replicas_ready(item)
        elif item.status.conditions:
            return ResourceItem.check_object_conditions(item)
        else:
            raise NotImplementedError(f"Unimplemented resource readiness check for {item.kind}  {item.metadata.name}.")

    def is_ready(self, refresh: bool = False) -> CheckResult:
        """Check if the resource data successfully satisfies the ready state."""
        if refresh:
            self.refresh()
        return self.check_object_is_ready(self)
