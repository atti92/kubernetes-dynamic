from __future__ import annotations

from datetime import datetime
from typing import Dict, List

from ..resource_value import ResourceValue


class V1ManagedFieldsEntry(ResourceValue):
    apiVersion: str
    fieldsType: str
    fieldsV1: object
    manager: str
    operation: str
    subresource: str
    time: datetime


class V1OwnerReference(ResourceValue):
    kind: str
    metadata: V1ObjectMeta
    blockOwnerDeletion: bool
    controller: bool
    name: str
    uid: str


class V1ObjectMeta(ResourceValue):
    annotations: Dict[str, str]
    creationTimestamp: datetime
    deletionGracePeriodSeconds: int
    deletionTimestamp: datetime
    finalizers: List[str]
    generateName: str
    generation: int
    labels: Dict[str, str]
    managedFields: List[V1ManagedFieldsEntry]
    name: str
    namespace: str
    ownerReferences: List[V1OwnerReference]
    resourceVersion: str
    selfLink: str
    uid: str
