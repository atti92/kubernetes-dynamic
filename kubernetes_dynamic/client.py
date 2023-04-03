from __future__ import annotations

import json
import re
from pathlib import Path
from types import NoneType
from typing import Any, Callable, List, Optional, Type, TypeVar, overload

import pydantic
import yaml

import kubernetes_dynamic.models as models

from . import _kubernetes
from .config import K8sConfig
from .events import Event, Watch
from .exceptions import (
    ConfigException,
    ConflictError,
    EventTimeoutError,
    InvalidParameter,
    NotFoundError,
    ResourceNotUniqueError,
    UnprocessibleEntityError,
)
from .formatters import format_selector
from .models.common import ItemList, get_type
from .models.resource_item import CheckResult, ResourceItem
from .models.resource_value import ResourceValue
from .resource_api import ResourceApi

T = TypeVar("T", bound=ResourceItem)


MISSING = object()


def serialize_object(data, serializer: Type = None) -> ResourceItem | ItemList[ResourceItem]:
    kind = data["kind"]
    is_list = False
    if kind.endswith("List") and "items" in data:
        kind = kind[:-4]
        is_list = True

    api_version = data["apiVersion"]

    obj_type = serializer or get_type(kind, api_version, ResourceItem)

    if not is_list:
        return pydantic.parse_obj_as(obj_type, data)

    for item in data["items"]:
        item.setdefault("apiVersion", api_version)
        item.setdefault("kind", kind)
    items = pydantic.parse_obj_as(List[obj_type], data["items"])
    return ItemList(items, metadata=data["metadata"])


def meta_request(func):
    """Handles parsing response structure and translating API Exceptions"""

    def inner(self, *args, **kwargs):
        serialize = kwargs.pop("serialize", True)
        serializer = kwargs.pop("serializer", ResourceValue)
        response = func(self, *args, **kwargs)
        if not response:
            return None
        if not serialize:
            return response
        data = json.loads(response.data)
        return serialize_object(data, serializer)

    return inner


class K8sClient(object):
    _loaded: bool = False
    in_cluster: bool = False

    componentstatuses: ResourceApi[models.V1ComponentStatus]
    configmaps: ResourceApi[models.V1ConfigMap]
    endpoints: ResourceApi[models.V1Endpoints]
    events: ResourceApi[models.CoreV1Event]
    limitranges: ResourceApi[models.V1LimitRange]
    namespaces: ResourceApi[models.V1Namespace]
    nodes: ResourceApi[models.V1Node]
    persistentvolumeclaims: ResourceApi[models.V1PersistentVolumeClaim]
    persistentvolumes: ResourceApi[models.V1PersistentVolume]
    pods: ResourceApi[models.V1Pod]
    podtemplates: ResourceApi[models.V1PodTemplate]
    replicationcontrollers: ResourceApi[models.V1ReplicationController]
    resourcequotas: ResourceApi[models.V1ResourceQuota]
    secrets: ResourceApi[models.V1Secret]
    serviceaccounts: ResourceApi[models.V1ServiceAccount]
    services: ResourceApi[models.V1Service]
    mutatingwebhookconfigurations: ResourceApi[models.V1MutatingWebhookConfiguration]
    validatingwebhookconfigurations: ResourceApi[models.V1ValidatingWebhookConfiguration]
    customresourcedefinitions: ResourceApi[models.V1CustomResourceDefinition]
    apiservices: ResourceApi[models.V1APIService]
    controllerrevisions: ResourceApi[models.V1ControllerRevision]
    daemonsets: ResourceApi[models.V1DaemonSet]
    deployments: ResourceApi[models.V1Deployment]
    replicasets: ResourceApi[models.V1ReplicaSet]
    statefulsets: ResourceApi[models.V1StatefulSet]
    horizontalpodautoscalers: ResourceApi[models.V1HorizontalPodAutoscaler]
    cronjobs: ResourceApi[models.V1CronJob]
    jobs: ResourceApi[models.V1Job]
    certificatesigningrequests: ResourceApi[models.V1CertificateSigningRequest]
    leases: ResourceApi[models.V1Lease]
    endpointslices: ResourceApi[models.V1EndpointSlice]
    flowschemas: ResourceApi[models.V1beta2FlowSchema]
    prioritylevelconfigurations: ResourceApi[models.V1beta2PriorityLevelConfiguration]
    ingressclasses: ResourceApi[models.V1IngressClass]
    ingresses: ResourceApi[models.V1Ingress]
    networkpolicies: ResourceApi[models.V1NetworkPolicy]
    runtimeclasses: ResourceApi[models.V1RuntimeClass]
    poddisruptionbudgets: ResourceApi[models.V1PodDisruptionBudget]
    clusterrolebindings: ResourceApi[models.V1ClusterRoleBinding]
    clusterroles: ResourceApi[models.V1ClusterRole]
    rolebindings: ResourceApi[models.V1RoleBinding]
    roles: ResourceApi[models.V1Role]
    priorityclasses: ResourceApi[models.V1PriorityClass]
    csidrivers: ResourceApi[models.V1CSIDriver]
    csinodes: ResourceApi[models.V1CSINode]
    csistoragecapacities: ResourceApi[models.V1CSIStorageCapacity]
    storageclasses: ResourceApi[models.V1StorageClass]
    volumeattachments: ResourceApi[models.V1VolumeAttachment]

    def __init__(
        self,
        api_client: Optional[_kubernetes.ApiClient] = None,
        *,
        config_file: Optional[str] = None,
        config_dict: Optional[dict] = None,
        context: Optional[str] = None,
        cache_file=None,
        discoverer=None,
    ):
        discoverer = discoverer or _kubernetes.dynamic.LazyDiscoverer
        self.config = self.get_config(config_file, config_dict=config_dict, context=context)
        self.client = api_client or _kubernetes.ApiClient(configuration=self.config.configuration)
        self.configuration = self.client.configuration
        self.__discoverer = discoverer(self, cache_file)

    @property
    def resources(self):
        return self.__discoverer

    @property
    def version(self):
        return self.__discoverer.version

    @staticmethod
    def get_config_file() -> str:
        """Get kube config file."""
        return str(Path(_kubernetes.KUBE_CONFIG_DEFAULT_LOCATION).expanduser().resolve())

    @staticmethod
    def get_kube_config_loader(
        config_file: Optional[str] = None, config_dict: Optional[dict] = None, context: Optional[str] = None
    ) -> _kubernetes.InClusterConfigLoader | _kubernetes.KubeConfigLoader:
        if not config_dict and not config_file:
            config_file = K8sClient.get_config_file()
        try:
            in_cluster_loader = _kubernetes.InClusterConfigLoader(
                token_filename=_kubernetes.SERVICE_TOKEN_FILENAME,
                cert_filename=_kubernetes.SERVICE_CERT_FILENAME,
                try_refresh_token=True,
            )
            in_cluster_loader.load_and_set()
            K8sClient.in_cluster = True
            return in_cluster_loader
        except ConfigException:
            K8sClient.in_cluster = False
            return _kubernetes._get_kube_config_loader(config_file, config_dict, active_context=context)

    @staticmethod
    def find_context(name: Optional[str], loader: _kubernetes.KubeConfigLoader) -> Optional[str]:
        """Find a context by name, or get the default."""
        if not name:
            return None
        contexts = loader.list_contexts()
        for context in contexts:
            if not isinstance(context, dict):
                continue
            if "context" not in context:
                continue
            if context.get("name") == name or context["context"].get("cluster") == name:
                return context.get("name")
        raise RuntimeError(f"No context name='{name}' found!")

    def get_config(
        self,
        config_file: Optional[str] = None,
        *,
        config_dict: Optional[dict] = None,
        context: Optional[str] = None,
    ) -> K8sConfig:
        """Get kubernetes config.

        Args:
            config_file: File to load.
            config_dict: Load config from dict instead of using a file.
            context: Set kube context.
        """
        loader = K8sClient.get_kube_config_loader(config_file, config_dict, context=context)
        if isinstance(loader, _kubernetes.InClusterConfigLoader):
            return K8sConfig(configuration=_kubernetes.Configuration.get_default_copy())
        config_file = config_file or K8sClient.get_config_file()
        context = K8sClient.find_context(context, loader)
        loader.set_active_context(context)
        configuration = type.__call__(_kubernetes.Configuration)
        loader.load_and_set(configuration)
        return K8sConfig(
            configuration=configuration,
            context=str(loader.current_context["context"].get("cluster")),
            namespace=str(loader.current_context["context"].get("namespace", "default")),
        )

    @overload
    def get_api(
        self,
        name: Optional[str] = None,
        object_type: NoneType = None,
        api_version: Optional[str] = None,
        kind: Optional[str] = None,
        **filter_dict,
    ) -> ResourceApi[ResourceItem]:
        ...

    @overload
    def get_api(
        self,
        name: Optional[str] = None,
        object_type: Type[T] = None,
        api_version: Optional[str] = None,
        kind: Optional[str] = None,
        **filter_dict,
    ) -> ResourceApi[T]:
        ...

    def get_api(
        self,
        name: Optional[str] = None,
        object_type: Optional[Type[T]] = ResourceItem,
        api_version: Optional[str] = None,
        kind: Optional[str] = None,
        **filter_dict,
    ) -> ResourceApi[T]:
        if api_version:
            filter_dict["api_version"] = api_version
        if kind:
            filter_dict["kind"] = kind
        if name:
            filter_dict["name"] = name
        try:
            api = self.resources.get(**filter_dict)
        except ResourceNotUniqueError:
            api = [
                r
                for r in self.resources.search(**filter_dict)
                if r.preferred and isinstance(r, _kubernetes.dynamic.Resource)
            ][0]
        api._resource_type = object_type or get_type(str(api.kind), str(api.api_version), ResourceItem)  # type: ignore
        return api  # type: ignore

    def __getattr__(self, name: str) -> ResourceApi[ResourceItem]:
        if name.startswith("_"):
            raise AttributeError(name)
        return self.get_api(name)

    @property
    def events_events(self) -> ResourceApi[models.EventsV1Event]:
        return self.get_api("events", object_type=models.EventsV1Event, api_version="events.k8s.io/v1")

    def ensure_namespace_param(self, resource, namespace, body=None) -> Optional[str]:
        if not resource.namespaced:
            return None
        if namespace is MISSING:
            if body:
                namespace = body.get("metadata", {}).get("namespace", self.config.namespace)
            else:
                namespace = self.config.namespace
        if not namespace:
            raise ValueError("Namespace is required for {}.{}".format(resource.group_version, resource.kind))
        return namespace

    def ensure_name_param(self, resource, name, body=None) -> str:
        if not name and body:
            name = body.get("metadata", {}).get("name")
        if not name:
            raise ValueError("Name is required for {}.{}".format(resource.group_version, resource.kind))
        return name

    def serialize_body(self, body):
        """Serialize body to raw dict so apiserver can handle it

        :param body: kubernetes resource body, current support: Union[Dict, ResourceValue]
        """
        if callable(getattr(body, "to_dict", None)):
            return body.to_dict()
        return body or {}

    def read(self, resource: ResourceApi, name=None, namespace=MISSING, **kwargs):
        namespace = self.ensure_namespace_param(resource, namespace)
        path = resource.path(name=name, namespace=namespace)
        return self.request("get", path, **kwargs)

    def get(self, resource: ResourceApi, name=None, namespace=MISSING, **kwargs):
        try:
            return self.read(resource, name, namespace, **kwargs)
        except NotFoundError:
            return None

    def find(self, resource: ResourceApi, pattern, namespace=MISSING, **kwargs):
        items = []
        data = self.get(resource, namespace=namespace, **kwargs)
        if not data:
            return items
        for item in data:
            if re.match(pattern, item.metadata.name):
                items.append(item)
        return items

    def create(self, resource: ResourceApi, body=None, namespace=MISSING, **kwargs):
        body = self.serialize_body(body)
        namespace = self.ensure_namespace_param(resource, namespace, body)
        path = resource.path(namespace=namespace)
        return self.request("post", path, body=body, **kwargs)

    def delete(
        self,
        resource: ResourceApi,
        name=None,
        namespace=MISSING,
        body=None,
        label_selector=None,
        field_selector=None,
        **kwargs,
    ):
        if not (name or label_selector or field_selector):
            raise ValueError("At least one of name|label_selector|field_selector is required")
        if resource.namespaced and not (label_selector or field_selector):
            namespace = self.ensure_namespace_param(resource, namespace)
        path = resource.path(name=name, namespace=namespace)
        return self.request(
            "delete", path, body=body, label_selector=label_selector, field_selector=field_selector, **kwargs
        )

    def replace(self, resource: ResourceApi, body=None, name=None, namespace=MISSING, **kwargs):
        body = self.serialize_body(body)
        name = self.ensure_name_param(resource, name, body)
        namespace = self.ensure_namespace_param(resource, namespace, body)
        path = resource.path(name=name, namespace=namespace)
        return self.request("put", path, body=body, **kwargs)

    def patch(self, resource: ResourceApi, body=None, name=None, namespace=MISSING, **kwargs):
        body = self.serialize_body(body)
        name = self.ensure_name_param(resource, name, body)
        namespace = self.ensure_namespace_param(resource, namespace, body)

        content_type = kwargs.pop("content_type", "application/strategic-merge-patch+json")
        path = resource.path(name=name, namespace=namespace)

        return self.request("patch", path, body=body, content_type=content_type, **kwargs)

    def server_side_apply(
        self, resource: ResourceApi, body=None, name=None, namespace=MISSING, force_conflicts=None, **kwargs
    ):
        body = self.serialize_body(body)
        name = self.ensure_name_param(resource, name, body)
        namespace = self.ensure_namespace_param(resource, namespace, body)

        # force content type to 'application/apply-patch+yaml'
        kwargs.update({"content_type": "application/apply-patch+yaml"})
        path = resource.path(name=name, namespace=namespace)

        return self.request("patch", path, body=body, force_conflicts=force_conflicts, **kwargs)

    def watch(
        self,
        resource: ResourceApi,
        namespace=MISSING,
        name=None,
        label_selector=None,
        field_selector=None,
        resource_version=None,
        timeout=None,
        watcher=None,
    ):
        namespace = self.ensure_namespace_param(resource, namespace)
        if name:
            field_selector = field_selector or ""
            field_selector += f",metadata.name={name}"
        watcher = watcher or Watch(self.client, resource._resource_type)
        if watcher and not resource_version:
            resource_version = watcher.resource_version
        return watcher.stream(
            resource.get,
            namespace=namespace or self.config.namespace,
            name=None,
            field_selector=field_selector,
            label_selector=label_selector,
            resource_version=resource_version,
            serialize=False,
            timeout_seconds=timeout,
        )

    def wait_until(
        self,
        resource: ResourceApi,
        *,
        namespace=MISSING,
        name=None,
        check: Callable[[Event], CheckResult],
        field_selector=None,
        label_selector=None,
        timeout: int = 30,
        **kwargs,
    ) -> Event:
        """Wait until a certain custom check returns true for a resource returned by the stream."""
        namespace = self.ensure_namespace_param(resource, namespace)
        field_selectors = [] if not field_selector else [format_selector(field_selector)]
        if name:
            field_selectors.append(f"metadata.name={name}")

        last = None
        result = None
        for event in resource.watch(
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

    def stream(self, method, name=None, namespace=MISSING, *args, **kwargs):
        from kubernetes.stream.ws_client import WSResponse, websocket_call

        prev_request = self.client.request
        try:

            def _websocket_call(*args, **kwargs):  # pragma: no cover
                ws_client = websocket_call(self.configuration, *args, **kwargs)
                ws_client.run_forever(timeout=kwargs.get("_request_timeout", 0))  # type: ignore
                return WSResponse("%s" % "".join(ws_client.read_all()))  # type: ignore

            self.client.request = _websocket_call
            return method(
                *args,
                name=name,
                namespace=namespace,
                query_params=[(k, v) for k, v in kwargs.items()],
                _preload_content=True,
                serialize=False,
            ).data

        finally:
            self.client.request = prev_request

    @meta_request
    def request(self, method, path, body=None, **params) -> Any:
        if not path.startswith("/"):
            path = "/" + path

        path_params = params.get("path_params", {})
        query_params = params.get("query_params", [])
        options = (
            "_continue",
            "pretty",
            "include_uninitialized",
            "field_selector",
            "label_selector",
            "limit",
            "resource_version",
            "timeout_seconds",
            "watch",
            "grace_period_seconds",
            "propagation_policy",
            "orphan_dependents",
            "dry_run",
            "field_manager",
            "force_conflicts",
        )
        for key in options:
            if params.get(key):
                query_params.append((key.lstrip("_"), params[key]))

        header_params = params.get("header_params", {})
        form_params = []
        local_var_files = {}

        # Checking Accept header.
        new_header_params = dict((key.lower(), value) for key, value in header_params.items())
        if "accept" not in new_header_params:
            header_params["Accept"] = self.client.select_header_accept(
                [
                    "application/json",
                    "application/yaml",
                ]
            )

        # HTTP header `Content-Type`
        header_params["Content-Type"] = params.get("content_type", self.client.select_header_content_type(["*/*"]))

        # Authentication setting
        auth_settings = ["BearerToken"]

        api_response = self.client.call_api(
            path,
            method.upper(),
            path_params,
            query_params,
            header_params,
            body=body,
            post_params=form_params,
            async_req=params.get("async_req"),
            files=local_var_files,
            auth_settings=auth_settings,
            _preload_content=False,
            _return_http_data_only=params.get("_return_http_data_only", True),
            _request_timeout=params.get("_request_timeout"),
        )
        return api_response.get() if params.get("async_req") else api_response  # type: ignore

    def apply(
        self,
        *,
        namespace: Optional[str | object] = MISSING,
        file_path: Optional[str | Path] = None,
        data: Optional[dict | list | ResourceItem] = None,
    ) -> list[ResourceItem]:
        """Apply a kubernetes resource."""
        if file_path is not None and data is not None:
            raise InvalidParameter("`file_path` and `data` is mutually exclusive.")
        if not data:
            if not file_path:
                raise InvalidParameter("`file_path` or `data` must be provided.")
            if not Path(file_path).exists():
                raise FileNotFoundError(file_path)
            with open(file_path) as fp:
                data = list(yaml.full_load_all(fp))
        if not isinstance(data, list):
            data = [data]

        items = []
        for item in data:
            resource = self.get_api(kind=item["kind"], api_version=item["apiVersion"].split("/")[-1])
            items.append(self._apply(resource, item, namespace))
        return items

    def _apply(
        self, resource: ResourceApi, body: dict | ResourceItem, namespace: Optional[str | object] = MISSING, **kwargs
    ) -> ResourceItem:
        namespace = self.ensure_namespace_param(resource, namespace)
        body["metadata"].setdefault("annotations", {})
        name = body["metadata"]["name"]
        try:
            return resource.create(body=body, namespace=namespace, **kwargs)
        except ConflictError:
            pass
        try:
            return resource.patch(name=name, body=body, namespace=namespace, **kwargs)
        except UnprocessibleEntityError:
            pass

        resource.delete(name=name, namespace=namespace, **kwargs)
        return resource.create(body=body, namespace=namespace, **kwargs)
