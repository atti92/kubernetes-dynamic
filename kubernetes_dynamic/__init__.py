__all__ = ["K8sClient", "K8sConfig", "models", "cl", "CheckResult", "ResourceItem", "ResourceValue"]

from . import models
from .client import K8sClient
from .config import K8sConfig
from .resource import CheckResult, ResourceItem
from .resource_value import ResourceValue

cl: K8sClient


def __getattr__(name: str):
    if name == "cl":
        global cl
        cl = K8sClient()
        return cl
    raise AttributeError(name)
