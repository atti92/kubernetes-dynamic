from __future__ import annotations

from typing import TYPE_CHECKING, Optional, Tuple, cast

from pydantic import Field

from kubernetes_dynamic.formatters import format_selector
from kubernetes_dynamic.models.common import ItemList, V1ObjectMeta, get_default
from kubernetes_dynamic.models.resource_item import ResourceItem

if TYPE_CHECKING:
    from .all import V1ServiceSpec, V1ServiceStatus
    from .pod import V1Pod


class V1Service(ResourceItem):
    metadata: V1ObjectMeta = Field(default_factory=lambda: V1ObjectMeta())
    spec: V1ServiceSpec = Field(default_factory=lambda: get_default("V1ServiceSpec"))
    status: V1ServiceStatus = Field(default_factory=lambda: get_default("V1ServiceStatus"))

    def get_pods(self) -> ItemList[V1Pod]:
        label_selector = self.spec.selector
        return self._client.pods.get(label_selector=format_selector(label_selector))

    def get_access(self, port: str | int) -> Optional[Tuple[str, str, int]]:
        for pod in self.get_pods():
            if pod.status.phase != "Running":
                continue
            port_number = pod.get_port(port)
            if not port_number:
                continue
            return (
                pod.metadata.name,
                cast(str, pod.status.podIP),
                port_number,
            )
        return None
