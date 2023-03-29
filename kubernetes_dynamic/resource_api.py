from __future__ import annotations

from typing import (
    Any,
    Dict,
    Generic,
    Iterator,
    List,
    Optional,
    Tuple,
    Type,
    TypeVar,
    overload,
)

from kubernetes.watch import Watch
from typing_extensions import Protocol

from .resource_value import ResourceValue

R = TypeVar("R", bound=ResourceValue)


class Event(ResourceValue, Generic[R]):
    """Kubernetes event object."""

    type: str
    raw_object: Dict[str, Any]
    object: R


class ResourceApi(Generic[R], Protocol):
    """See kubernetes.dynamic.Resource."""

    _resource_type: Type[R]
    kind: str
    api_version: str
    namespaced: bool

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
    def get(
        self,
        name: None = None,
        namespace: Optional[str] = None,
        *,
        label_selector: Optional[str] = None,
        field_selector: Optional[str] = None,
        **kwargs,
    ) -> List[R]:
        ...  # pragma: no cover

    @overload
    def get(self, name: str, namespace: Optional[str] = None, **kwargs) -> Optional[R]:
        ...  # pragma: no cover

    def create(self, body: dict | R, namespace: Optional[str] = None, **kwargs) -> R:
        ...  # pragma: no cover

    @overload
    def delete(self, name: str, namespace: Optional[str] = None, body: Optional[dict | R] = None, **kwargs) -> R:
        ...  # pragma: no cover

    @overload
    def delete(
        self,
        *,
        namespace: Optional[str] = None,
        body: Optional[dict | R] = None,
        label_selector: str,
        field_selector: Optional[str] = None,
        **kwargs,
    ) -> List[R]:
        ...  # pragma: no cover

    @overload
    def delete(
        self,
        *,
        namespace: Optional[str] = None,
        body: Optional[dict | R] = None,
        label_selector: Optional[str] = None,
        field_selector: str,
        **kwargs,
    ) -> List[R]:
        ...  # pragma: no cover

    def replace(self, body: dict | R, name: Optional[str] = None, namespace: Optional[str] = None, **kwargs) -> R:
        ...  # pragma: no cover

    def patch(self, body: dict | R, name: Optional[str] = None, namespace: Optional[str] = None, **kwargs) -> R:
        ...  # pragma: no cover

    def server_side_apply(
        self,
        body: dict | R,
        name: Optional[str] = None,
        namespace: Optional[str] = None,
        force_conflicts: Optional[bool] = None,
        **kwargs,
    ) -> R:
        ...  # pragma: no cover

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
        ...  # pragma: no cover

    def validate(self, definition: dict, version: Optional[str] = None, strict: bool = False) -> Tuple[List, List]:
        ...  # pragma: no cover
