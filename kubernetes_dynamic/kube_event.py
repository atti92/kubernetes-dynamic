from enum import Enum
from typing import Any, Dict, Generic, TypeVar

from kubernetes_dynamic.resource_value import ResourceValue

R = TypeVar("R", bound=ResourceValue)


class EventType(Enum):
    """Kubernetes Event type.

    This is related to how Kubernetes events are managed in Kubernetes.
    * ADDED - when a Kubernetes Event is created
    * MODIFIED - when a Kubernetes Event is modified
    * DELETED - when a Kubernetes Event is deleted
    """

    ADDED = "ADDED"
    MODIFIED = "MODIFIED"
    DELETED = "DELETED"


class Event(ResourceValue, Generic[R]):
    """Kubernetes event object."""

    type: EventType
    raw_object: Dict[str, Any]
    object: R
