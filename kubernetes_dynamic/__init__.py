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
    "Watch",
]

from . import exceptions, models
from ._kubernetes import Watch
from .client import K8sClient
from .config import K8sConfig
from .resource import CheckResult, ResourceItem
from .resource_api import Event, ResourceApi
from .resource_value import ResourceValue

cl: K8sClient


def __getattr__(name: str):
    if name == "cl":
        global cl
        cl = K8sClient()
        return cl
    raise AttributeError(name)
