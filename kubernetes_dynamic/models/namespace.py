from __future__ import annotations

from typing import TYPE_CHECKING, Dict, cast

from pydantic import Field

from kubernetes_dynamic.models.common import V1ObjectMeta, get_default

from ..exceptions import ConflictError
from .resource_item import ResourceItem

if TYPE_CHECKING:
    from .all import V1NamespaceSpec, V1NamespaceStatus


class V1Namespace(ResourceItem):
    spec: V1NamespaceSpec = Field(default_factory=lambda: get_default("V1NamespaceSpec"))
    status: V1NamespaceStatus = Field(default_factory=lambda: get_default("V1NamespaceStatus"))

    def annotate(self, annotations_dict: Dict[str, str]) -> V1Namespace:
        """Add annotation(s) to the namespace."""
        self.refresh_()
        existing: Dict[str, str] = self.metadata.annotations or {}
        existing.update(annotations_dict)
        return self.patch_()

    @classmethod
    def ensure(cls, name: str) -> V1Namespace:
        item = V1Namespace(metadata=cast(V1ObjectMeta, {"name": name}))
        try:
            return item.create_()
        except ConflictError:
            return item.refresh_()
