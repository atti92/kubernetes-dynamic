from __future__ import annotations

from typing import TYPE_CHECKING

from ..resource import ResourceItem
from .common import V1ObjectMeta

if TYPE_CHECKING:
    from . import V1StatefulSetSpec, V1StatefulSetStatus


class V1StatefulSet(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1StatefulSetSpec
    status: V1StatefulSetStatus
