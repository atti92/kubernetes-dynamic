from __future__ import annotations

import functools
import inspect
import json
from pathlib import Path
from typing import Callable, List, Optional, Type, TypeVar

import pydantic
import yaml

from kubernetes_dynamic.formatters import format_selector
from kubernetes_dynamic.models.common import ItemList

from . import _kubernetes, models
from .config import K8sConfig
from .exceptions import (
    ConfigException,
    ConflictError,
    EventTimeoutError,
    InvalidParameter,
    NotFoundError,
    ResourceNotUniqueError,
    UnprocessibleEntityError,
)
from .resource import CheckResult, ResourceItem
from .resource_api import Event, ResourceApi

T = TypeVar("T", bound=ResourceItem)


def serialize_object(data, resource_api: Optional[ResourceApi] = None) -> ResourceItem | ItemList[ResourceItem]:
    kind = data["kind"]
    api_version = data["apiVersion"]

    if resource_api and hasattr(resource_api, "_resource_type") and resource_api._resource_type:
        obj_type = resource_api._resource_type
    else:
        obj_type = models.get_type(kind, api_version, ResourceItem)

    if kind.endswith("List") and "items" in data:
        kind = kind[:-4]
        for item in data["items"]:
            item.setdefault("apiVersion", api_version)
            item.setdefault("kind", kind)
        items = pydantic.parse_obj_as(List[obj_type], data["items"])
        return ItemList(items, metadata=data["metadata"])
    return pydantic.parse_obj_as(obj_type, data)


def serialize(func):
    @functools.wraps(func)
    def wrapped(client: K8sClient, resource_api: ResourceApi, *args, serialize=True, **kwargs):
        response = func(client, resource_api, *args, serialize=False, **kwargs)
        if not response:
            return None
        if not serialize:
            return response
        data = json.loads(response.data)
        return serialize_object(data, resource_api)

    return wrapped


def default_namespaced(func):
    @functools.wraps(func)
    def wrapped(client: K8sClient, resource: ResourceApi, *args, **kwargs):
        if not resource.namespaced or "namespace" in kwargs:
            return func(client, resource, *args, **kwargs)
        params = inspect.signature(func).parameters
        namespace_param = params.get("namespace")
        body_param = params.get("body")
        args = list(args)
        namespace = client.config.namespace
        if body_param and body_param.kind == body_param.POSITIONAL_OR_KEYWORD:
            arg_index = list(params).index("body") - 2
            body = kwargs.get("body", args[arg_index] if len(args) > arg_index else {}) or {}
            namespace = body.get("metadata", {}).get("namespace", namespace)
        if namespace_param and namespace_param.kind == namespace_param.POSITIONAL_OR_KEYWORD:
            arg_index = list(params).index("namespace") - 2
            if len(args) > arg_index:
                args[arg_index] = args[arg_index] or namespace
            else:
                kwargs["namespace"] = kwargs.get("namespace", namespace)
        return func(client, resource, *args, **kwargs)

    return wrapped


class K8sClient(_kubernetes.dynamic.DynamicClient):
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
    ):
        self.config = self.get_config(config_file, config_dict=config_dict, context=context)
        self.client = api_client or _kubernetes.ApiClient(configuration=self.config.configuration)
        super().__init__(self.client)

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

    def get_api(
        self,
        name: Optional[str] = None,
        object_type: Optional[Type[T]] = None,
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
        api._resource_type = object_type or models.get_type(  # type: ignore
            str(api.kind), str(api.api_version), ResourceItem
        )
        return api  # type: ignore

    def __getattr__(self, name: str) -> ResourceApi[ResourceItem]:
        if name.startswith("_"):
            raise AttributeError(name)
        return self.get_api(name)

    @property
    def events_events(self) -> ResourceApi[models.EventsV1Event]:
        return self.get_api("events", object_type=models.EventsV1Event, api_version="events.k8s.io/v1")

    @serialize
    @default_namespaced
    def get(self, resource: ResourceApi, name=None, namespace=None, **kwargs):
        try:
            return super().get(resource, name, namespace, **kwargs)
        except NotFoundError:
            return None

    @serialize
    @default_namespaced
    def create(self, resource: ResourceApi, body=None, namespace=None, **kwargs):
        return super().create(resource, body, namespace, **kwargs)

    @serialize
    @default_namespaced
    def delete(
        self,
        resource: ResourceApi,
        name=None,
        namespace=None,
        body=None,
        label_selector=None,
        field_selector=None,
        **kwargs,
    ):
        return super().delete(resource, name, namespace, body, label_selector, field_selector, **kwargs)

    @serialize
    @default_namespaced
    def replace(self, resource: ResourceApi, body=None, name=None, namespace=None, **kwargs):
        return super().replace(resource, body, name, namespace, **kwargs)

    @serialize
    @default_namespaced
    def patch(self, resource: ResourceApi, body=None, name=None, namespace=None, **kwargs):
        return super().patch(resource, body, name, namespace, **kwargs)

    @serialize
    @default_namespaced
    def server_side_apply(
        self, resource: ResourceApi, body=None, name=None, namespace=None, force_conflicts=None, **kwargs
    ):
        return super().server_side_apply(resource, body, name, namespace, force_conflicts, **kwargs)

    @default_namespaced
    def watch(
        self,
        resource: ResourceApi,
        namespace=None,
        name=None,
        label_selector=None,
        field_selector=None,
        resource_version=None,
        timeout=None,
        watcher=None,
        **kwargs,
    ):
        if name:
            field_selector = field_selector or ""
            field_selector += f",metadata.name={name}"
        for item in super().watch(
            resource,
            namespace,
            None,
            label_selector,
            field_selector,
            resource_version,
            timeout,
            watcher,
        ):
            item["object"] = serialize_object(item["object"], resource)  # type: ignore
            yield Event(**item)  # type: ignore

    def wait_until(
        self,
        resource: ResourceApi,
        *,
        namespace=None,
        name=None,
        check: Callable[[Event], CheckResult],
        field_selector=None,
        label_selector=None,
        timeout: int = 30,
        **kwargs,
    ) -> Event:
        """Wait until a certain custom check returns true for a resource returned by the stream."""
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

    def stream(self, method, name=None, namespace=None, *args, **kwargs):
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

    def apply(
        self,
        *,
        namespace: Optional[str] = None,
        file_path: Optional[str | Path] = None,
        data: Optional[dict | list] = None,
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
        elif isinstance(data, dict):
            data = [data]

        items = []
        for item in data:
            resource = self.get_api(kind=item["kind"], api_version=item["apiVersion"].split("/")[-1])
            items.append(self._apply(resource, item, namespace))
        return items

    @default_namespaced
    def _apply(self, resource: ResourceApi, body: dict, namespace: Optional[str] = None, **kwargs) -> ResourceItem:
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
