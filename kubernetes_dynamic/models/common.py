from __future__ import annotations

from collections import UserList
from datetime import datetime
from typing import Any, Dict, Generic, Iterator, List, Optional, TypeVar

import pydantic
from pydantic import Field

from .resource_value import ResourceValue

R = TypeVar("R", bound=ResourceValue)


class V1ManagedFieldsEntry(ResourceValue):
    apiVersion: str = "v1"
    fieldsType: Optional[str] = None
    fieldsV1: Optional[object] = None
    manager: Optional[str] = None
    operation: Optional[str] = None
    subresource: Optional[str] = None
    time: Optional[datetime] = None


class V1OwnerReference(ResourceValue):
    apiVersion: str = "v1"
    kind: str = "OwnerReference"
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    blockOwnerDeletion: Optional[bool] = None
    controller: Optional[bool] = None
    name: str
    uid: Optional[str] = None


class V1ObjectMeta(ResourceValue):
    annotations: Dict[str, str] = Field(default_factory=dict)
    creationTimestamp: Optional[datetime] = None
    deletionGracePeriodSeconds: Optional[int] = None
    deletionTimestamp: Optional[datetime] = None
    finalizers: List[str] = Field(default_factory=list)
    generateName: Optional[str] = None
    generation: Optional[int] = None
    labels: Dict[str, str] = Field(default_factory=dict)
    managedFields: List[V1ManagedFieldsEntry] = Field(default_factory=list)
    name: str = ""
    namespace: Optional[str] = None
    ownerReferences: List[V1OwnerReference] = Field(default_factory=list)
    resourceVersion: Optional[str] = None
    selfLink: Optional[str] = None
    uid: Optional[str] = None


class V1ListMeta(ResourceValue):
    remainingItemCount: int = 0
    resourceVersion: Optional[str] = None
    selfLink: Optional[str] = None


class ItemList(UserList, Generic[R]):
    metadata: V1ListMeta = Field(default_factory=V1ListMeta)

    def __init__(self, initlist, metadata):
        self.metadata = pydantic.parse_obj_as(V1ListMeta, metadata)
        super().__init__(initlist)

    def pop(self) -> R:
        return super().pop()

    def __getitem__(self, index) -> R:
        return super().__getitem__(index)

    def __iter__(self) -> Iterator[R]:
        return super().__iter__()


def get_default(name: str):
    from . import all

    return getattr(all, name)()


def get_type(kind: str, version: str, default: Any = None) -> Any:
    from . import all

    return all.mapping.get(kind, {}).get(version, default)
