from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from ..resource import ResourceItem

if TYPE_CHECKING:
    from . import V1IngressSpec, V1IngressStatus, V1ObjectMeta


class V1Ingress(ResourceItem):
    metadata: V1ObjectMeta
    spec: V1IngressSpec
    status: V1IngressStatus

    @classmethod
    def get_default_host(cls) -> Optional[str]:
        """Get default ingress host."""
        items = cls.default_client().ingresses.get()
        if not items:
            return None
        ingress = items[0]
        return f"https://{ingress.spec.rules[0].host}"
