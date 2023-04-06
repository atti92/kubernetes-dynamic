from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, List, Optional, Type, TypeVar, overload

import pydantic
import yaml

import kubernetes_dynamic.kube.ws_client as ws_client
import kubernetes_dynamic.models as models

from . import _kubernetes
from .config import K8sConfig
from .exceptions import (
    ConfigException,
    InvalidParameter,
    ResourceNotUniqueError,
)
from .kube.resource_api import MISSING, ResourceApi, _Missing
from .models.common import ItemList, get_type
from .models.resource_item import ResourceItem

T = TypeVar("T", bound=ResourceItem)


def serialize_object(
    data, serializer: Optional[Type[ResourceItem] | Callable] = None
) -> ResourceItem | ItemList[ResourceItem]:
    if serializer and not isinstance(serializer, Type):
        try:
            return serializer(data)
        except TypeError:
            return serializer(data, data)
    kind = data.get("kind", "")
    is_list = False
    if kind.endswith("List") and "items" in data:
        kind = kind[:-4]
        is_list = True

    api_version = data.get("apiVersion", "v1")

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
        serializer = kwargs.pop("serializer", None)
        response = func(self, *args, **kwargs)
        if not response:
            return None
        if not serialize:
            return response
        try:
            data = json.loads(response.data)
            return serialize_object(data, serializer)
        except json.JSONDecodeError:
            return response.data

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
        discoverer = discoverer or _kubernetes.LazyDiscoverer
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
        object_type: None = None,
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
                if r.preferred and isinstance(r, _kubernetes.ResourceApi)
            ][0]
        api.resource_type = object_type or get_type(str(api.kind), str(api.api_version), ResourceItem)  # type: ignore
        return api  # type: ignore

    def __getattr__(self, name: str) -> ResourceApi[ResourceItem]:
        if name.startswith("_"):
            raise AttributeError(name)
        return self.get_api(name)

    @property
    def events_events(self) -> ResourceApi[models.EventsV1Event]:
        return self.get_api("events", object_type=models.EventsV1Event, api_version="events.k8s.io/v1")

    def websocket(self, func: Callable, name=None, namespace=MISSING, *args, **kwargs) -> ws_client.WSClient:
        prev_request = self.client.request
        try:

            def _websocket(*args, **kwargs):  # pragma: no cover
                try:
                    client = ws_client.websocket_call(self.configuration, *args, **kwargs)
                except Exception as e:
                    raise e
                return client

            self.client.request = _websocket
            return func(
                *args,
                name=name,
                namespace=namespace,
                query_params=[(k, v) for k, v in kwargs.items() if v is not None],
                _preload_content=True,
                serialize=False,
            )
        finally:
            self.client.request = prev_request

    def stream(self, func: Callable, name=None, namespace=MISSING, *args, **kwargs) -> str:
        client = self.websocket(func, name, namespace, *args, **kwargs)
        client.run_forever(timeout=kwargs.get("_request_timeout", 0))  # type: ignore
        return ws_client.WSResponse("%s" % "".join(client.read_all())).data

    @meta_request
    def request(self, method: str, path: str, body=None, **params) -> Any:
        if not path.startswith("/"):
            path = "/" + path

        path_params = params.pop("path_params", {})
        query_params = params.pop("query_params", [])

        header_params = params.pop("header_params", {})
        form_params = []
        local_var_files = {}

        # Checking Accept header.
        new_header_params = dict((key.lower(), value) for key, value in header_params.items())
        if "accept" not in new_header_params:
            header_params["Accept"] = "application/json"

        # HTTP header `Content-Type`
        header_params["Content-Type"] = params.pop("content_type", "application/json")
        async_req = params.pop("async_req", False)
        _return_http_data_only = params.pop("_return_http_data_only", True)
        _request_timeout = params.pop("_request_timeout", None)

        # Authentication setting
        auth_settings = ["BearerToken"]

        for key, value in params.items():
            if value is not None:
                query_params.append((key.lstrip("_"), value))

        api_response = self.client.call_api(
            path,
            method.upper(),
            path_params,
            query_params,
            header_params,
            body=body,
            post_params=form_params,
            async_req=async_req,
            files=local_var_files,
            auth_settings=auth_settings,
            _preload_content=False,
            _return_http_data_only=_return_http_data_only,
            _request_timeout=_request_timeout,
        )
        return api_response.get() if async_req else api_response  # type: ignore

    def apply(
        self,
        *,
        namespace: Optional[str | _Missing] = MISSING,
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
            items.append(resource.apply(item, namespace))
        return items


