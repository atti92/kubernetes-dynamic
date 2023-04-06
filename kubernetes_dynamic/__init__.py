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
    "__version__"
]

from . import exceptions, models
from ._version import __version__
from .client import K8sClient
from .config import K8sConfig
from .events import Event, EventType, Watch
from .kube.resource_api import ResourceApi
from .models.resource_item import CheckResult, ResourceItem
from .models.resource_value import ResourceValue

cl: K8sClient


def __getattr__(name: str):
    if name == "cl":
        global cl
        cl = K8sClient()
        return cl
    raise AttributeError(name)

