from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from kubernetes_dynamic.formatters import format_selector

from .common import ItemList, V1ObjectMeta, get_default
from .resource_item import ResourceItem

if TYPE_CHECKING:
    from .all import V1ReplicaSetSpec, V1ReplicaSetStatus
    from .pod import V1Pod


class V1ReplicaSet(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1ReplicaSetSpec = Field(default_factory=lambda: get_default("V1ReplicaSetSpec"))
    status: V1ReplicaSetStatus = Field(default_factory=lambda: get_default("V1ReplicaSetStatus"))

    def get_pods(self) -> ItemList[V1Pod]:
        label_selector = self.spec.selector.matchLabels
        return self._client.pods.get(label_selector=format_selector(label_selector))
