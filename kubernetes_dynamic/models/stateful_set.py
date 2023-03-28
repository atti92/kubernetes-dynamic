from __future__ import annotations

from typing import TYPE_CHECKING

from ..resource import ResourceItem

if TYPE_CHECKING:
    from . import V1ObjectMeta, V1StatefulSetSpec, V1StatefulSetStatus


class V1StatefulSet(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1StatefulSetSpec
    status: V1StatefulSetStatus
