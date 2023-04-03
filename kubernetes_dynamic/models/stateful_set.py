from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import Field

from .common import get_default
from .resource_item import ResourceItem

if TYPE_CHECKING:
    from .all import V1StatefulSetSpec, V1StatefulSetStatus


class V1StatefulSet(ResourceItem):
    spec: V1StatefulSetSpec = Field(default_factory=lambda: get_default("V1StatefulSetSpec"))
    status: V1StatefulSetStatus = Field(default_factory=lambda: get_default("V1StatefulSetStatus"))
