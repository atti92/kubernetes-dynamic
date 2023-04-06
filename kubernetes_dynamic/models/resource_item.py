from __future__ import annotations

import re
import typing
from typing import Callable, Optional

import pydantic
from typing_extensions import Self

from kubernetes_dynamic.events import Event, EventType

from ..exceptions import NotFoundError
from .common import V1ObjectMeta
from .resource_value import ResourceValue

if typing.TYPE_CHECKING:
    from kubernetes_dynamic.kube.resource_api import ResourceApi

    from ..client import K8sClient


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

    apiVersion: str = ""
    kind: str = ""
    metadata: V1ObjectMeta = pydantic.Field(default_factory=V1ObjectMeta)
    status: ResourceValue = pydantic.Field(default_factory=ResourceValue)

    _client_instance: Optional[K8sClient] = pydantic.PrivateAttr()
    _api_instance: Optional[ResourceApi] = pydantic.PrivateAttr()

    def __init__(
        self,
        definition: dict | ResourceValue | None = None,
        client=None,
        **kwargs,
    ):
        final_def = ResourceItem.merge_definition_with_kwargs(definition, **kwargs)
        defaults = self.get_defaults()
        kind = final_def.get("kind") or self.kind or defaults.get("kind")
        if kind:
            final_def["kind"] = kind
        api_version = final_def.get("apiVersion") or self.apiVersion or defaults.get("apiVersion")
        if api_version:
            final_def["apiVersion"] = api_version

        super().__init__(**final_def)

        self._api_instance: Optional[ResourceApi] = None
        self._client_instance = client

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.metadata.name}, namespace={self.metadata.namespace})"

    @classmethod
    def get_defaults(cls):
        """Get some default values based on the class."""
        values = {}
        for cl in [cls] + list(cls.__bases__):
            parts = re.sub("([a-z0-9])([A-Z])", r"\1 \2", cl.__name__).split()
            match = [part for part in parts if re.match(r"^V\d.*", part)]
            if match:
                version = match[0]
                version_index = parts.index(version) + 1
                values["kind"] = "".join(parts[version_index:])
                values["apiVersion"] = version.lower()
                break
        return values

    @property
    def _api(self) -> ResourceApi:
        """Get resource api."""
        if (
            not self._api_instance
            or self._api_instance.api_version != self.apiVersion
            or self._api_instance.kind != self.kind
        ):
            self._api_instance = self._client.get_api(kind=self.kind, api_version=self.apiVersion)
        return self._api_instance

    @property
    def _client(self) -> K8sClient:
        """Get resource api."""
        if not self._client_instance:
            self._client_instance = self.default_client()
        return self._client_instance

    @classmethod
    def default_client(cls) -> K8sClient:
        """Create a default K8sClient."""
        from ..client import K8sClient

        return K8sClient()

    def refresh_(self) -> Self:
        """Refreshes the local instance with kubernetes data."""
        data = self.read_()
        if data is None:
            raise NotFoundError(self)
        return self._update_attrs(data)

    def patch_(self) -> Self:
        """Updates the Kubernetes resource."""
        return self._update_attrs(self._api.patch(name=self.metadata.name, body=self))

    def create_(self) -> Self:
        """Creates the object in Kubernetes."""
        return self._update_attrs(self._api.create(self))

    def read_(self) -> Optional[Self]:
        """Reads the object in Kubernetes."""
        return self._api.get(self.metadata.name, self.metadata.namespace)

    def delete_(self) -> Self:
        """Deletes the object from Kubernetes."""
        return self._api.delete(self.metadata.name, self.metadata.namespace)

    @staticmethod
    def check_object_conditions(item: ResourceItem) -> CheckResult:
        """Check object conditions."""
        name = item.metadata.name
        if not item.status or not item.status.conditions:
            return CheckResult(False, f"No conditions found on {item.kind} {name}.")
        for condition in item.status.conditions:  # type: ignore
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
                f"{item.kind} {name} only have {ready_replicas} ready replicas out of required {replicas}.",
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
            self.refresh_()
        return self.check_object_is_ready(self)

    def wait_until_status(self, status: str, timeout: int = 30) -> Event:
        """Wait until the resource is in a specific status."""

        def status_check(event: Event) -> CheckResult:
            result = event.raw_object["status"]["phase"] == status and event.type != EventType.DELETED
            if result:
                message = f"{self.kind} {self.metadata.name} is {status}."
            else:
                message = f"Last status of {self.kind} {self.metadata.name}: {event.raw_object['status']['phase']}"
            return CheckResult(result, message)

        return self.wait_until(check=status_check, timeout=timeout)

    def wait_until_ready(
        self,
        timeout: int = 30,
        **kwargs,
    ):
        """Waiting until resource is ready."""
        return self.wait_until(
            check=lambda event: self.check_object_is_ready(event.object),
            timeout=timeout,
            **kwargs,
        )

    def wait_until_not_ready(
        self,
        timeout: int = 30,
        **kwargs,
    ) -> Event:
        """Waiting until resource is not ready."""

        def not_ready(event: Event) -> CheckResult:
            result = self.check_object_is_ready(event.object)
            return CheckResult(not result, result.message)

        return self.wait_until(
            check=not_ready,
            timeout=timeout,
            **kwargs,
        )

    def wait_until(self, check: Callable[[Event], CheckResult], timeout: int = 30, **kwargs) -> Event:
        return self.api.wait_until(
            check=check,
            timeout=timeout,
            **kwargs,
        )
