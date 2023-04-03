from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from pydantic import Field

from kubernetes_dynamic.models.common import get_default

from .resource_item import ResourceItem

if TYPE_CHECKING:
    from .all import V1IngressSpec, V1IngressStatus


class V1Ingress(ResourceItem):
    spec: V1IngressSpec = Field(default_factory=lambda: get_default("V1IngressSpec"))
    status: V1IngressStatus = Field(default_factory=lambda: get_default("V1IngressStatus"))

    @classmethod
    def get_default_host(cls) -> Optional[str]:
        """Get default ingress host."""
        items = cls.default_client().ingresses.get()
        if not items:
            return None
        return items[0].url

    @property
    def url(self):
        """Get URL."""
        return f"https://{self.spec.rules[0].host}"
