__all__ = [
    "K8sClient",
    "K8sConfig",
    "models",
    "exceptions",
    "cl",
    "CheckResult",
    "ResourceItem",
    "ResourceValue",
    "ResourceApi",
    "Event",
    "EventType",
    "Watch",
]

from . import exceptions, models
from .client import K8sClient
from .config import K8sConfig
from .events import Event, EventType, Watch
from .models.resource_item import CheckResult, ResourceItem
from .models.resource_value import ResourceValue
from .resource_api import ResourceApi

cl: K8sClient


def __getattr__(name: str):
    if name == "cl":
        global cl
        cl = K8sClient()
        return cl
    raise AttributeError(name)
