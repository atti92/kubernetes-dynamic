from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from ..exceptions import ConflictError
from ..resource import ResourceItem
from .common import V1ObjectMeta

if TYPE_CHECKING:
    from . import V1NamespaceSpec, V1NamespaceStatus


class V1Namespace(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1NamespaceSpec
    status: V1NamespaceStatus

    def annotate(self, annotations_dict: Dict[str, str]) -> V1Namespace:
        """Add annotation(s) to the namespace."""
        self.refresh()
        existing: Dict[str, str] = self.metadata.annotations or {}
        existing.update(annotations_dict)
        return self.patch()

    @classmethod
    def ensure(cls, name: str) -> V1Namespace:
        item = V1Namespace(metadata={"name": name})
        try:
            return item.create()
        except ConflictError:
            return item.refresh()
