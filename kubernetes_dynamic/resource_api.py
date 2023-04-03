from __future__ import annotations

import typing
from types import NoneType
from typing import (
    Any,
    Iterator,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    overload,
)

from typing_extensions import Protocol

from kubernetes_dynamic.events import Watch
from kubernetes_dynamic.models.resource_value import ResourceValue

if typing.TYPE_CHECKING:
    from kubernetes_dynamic.client import K8sClient
    from kubernetes_dynamic.events import Event
    from kubernetes_dynamic.models.common import ItemList


R = TypeVar("R", bound=ResourceValue)


class ResourceApi(Protocol[R]):
    """See kubernetes.dynamic.Resource."""

    _resource_type: Type[R]
    kind: str
    api_version: str
    namespaced: bool
    client: K8sClient

    @property
    def resources(self) -> Any:
        ...  # pragma: no cover

    @property
    def version(self) -> str:
        ...  # pragma: no cover

    def ensure_namespace(self, namespace: str, body: dict | R) -> str:
        ...  # pragma: no cover

    def serialize_body(self, body: dict | R) -> dict:
        ...  # pragma: no cover

    @overload
    def read(
        self,
        name: None = None,
        namespace: Optional[str] = None,
        *,
        label_selector: Optional[str] = None,
        field_selector: Optional[str] = None,
        **kwargs,
    ) -> ItemList[R]:
        ...  # pragma: no cover

    @overload
    def read(self, name: str, namespace: Optional[str] = None, **kwargs) -> R:
        ...  # pragma: no cover

    @overload
    def read(self, name: str, namespace: Optional[str] = None, **kwargs) -> R:
        ...  # pragma: no cover

    def read(self, name: Optional[str] = None, namespace: Optional[str] = None, **kwargs) -> R | ItemList[R]:
        return self.client.read(self, name, namespace, **kwargs)  # pragma: no cover

    @overload
    def get(
        self,
        name: None = None,
        namespace: Optional[str] = None,
        *,
        label_selector: Optional[str] = None,
        field_selector: Optional[str] = None,
        **kwargs,
    ) -> ItemList[R]:
        ...  # pragma: no cover

    @overload
    def get(self, name: str, namespace: Optional[str] = None, **kwargs) -> Optional[R]:
        ...  # pragma: no cover

    @overload
    def get(self, name: str, namespace: Optional[str] = None, **kwargs) -> Optional[R]:
        ...  # pragma: no cover

    def get(self, name: Optional[str] = None, namespace: Optional[str] = None, **kwargs) -> Optional[R] | ItemList[R]:
        return self.client.get(self, name, namespace, **kwargs)  # pragma: no cover

    def find(self, pattern: str, namespace: Optional[str] = None, **kwargs) -> list[R]:
        return self.client.find(self, pattern, namespace, **kwargs)  # pragma: no cover

    def create(self, body: dict | R, namespace: Optional[str] = None, **kwargs) -> R:
        return self.client.create(self, body, namespace, **kwargs)  # pragma: no cover

    @overload
    def delete(self, name: str, namespace: Optional[str] = None, body: Optional[dict | R] = None, **kwargs) -> R:
        ...  # pragma: no cover

    @overload
    def delete(
        self,
        name: NoneType = None,
        namespace: Optional[str] = None,
        body: Optional[dict | R] = None,
        label_selector: Optional[str] = None,
        field_selector: Optional[str] = None,
        **kwargs,
    ) -> ItemList[R]:
        ...  # pragma: no cover

    def delete(
        self,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        body: Optional[dict | R] = None,
        label_selector: Optional[str] = None,
        field_selector: Optional[str] = None,
        **kwargs,
    ) -> ItemList[R] | R:
        return self.client.delete(
            self, namespace=namespace, body=body, label_selector=label_selector, field_selector=field_selector, **kwargs
        )  # pragma: no cover

    def replace(self, body: dict | R, name: Optional[str] = None, namespace: Optional[str] = None, **kwargs) -> R:
        return self.client.replace(self, body, name, namespace, **kwargs)  # pragma: no cover

    def patch(self, body: dict | R, name: Optional[str] = None, namespace: Optional[str] = None, **kwargs) -> R:
        return self.client.patch(self, body, name, namespace, **kwargs)  # pragma: no cover

    def server_side_apply(
        self,
        body: dict | R,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        force_conflicts: Optional[bool] = None,
        **kwargs,
    ) -> R:
        return self.client.server_side_apply(self, body, name, namespace, force_conflicts, **kwargs)  # pragma: no cover

    def watch(
        self,
        namespace: Optional[str] = None,
        name: Optional[str] = None,
        label_selector: Optional[str] = None,
        field_selector: Optional[str] = None,
        resource_version: Optional[str] = None,
        timeout: Optional[float] = None,
        watcher: Optional[Watch] = None,
    ) -> Iterator[Event[R]]:
        yield from self.client.watch(
            self, namespace, name, label_selector, field_selector, resource_version, timeout, watcher
        )  # pragma: no cover

    def validate(self, definition: dict, version: Optional[str] = None, strict: bool = False) -> Tuple[List, List]:
        ...  # pragma: no cover

    def path(self, name=None, namespace=None):
        ...  # pragma: no cover

    def __getattr__(self, name) -> ResourceApi:
        ...  # pragma: no cover

    @property
    def urls(self) -> dict[str, str]:
        ...  # pragma: no cover

    @property
    def group_version(self) -> str:
        ...  # pragma: no cover

    def to_dict(self) -> dict:
        ...  # pragma: no cover
