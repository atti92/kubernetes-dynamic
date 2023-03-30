from ._kubernetes import ConfigException as ConfigException
from ._kubernetes import ConflictError as ConflictError
from ._kubernetes import NotFoundError as NotFoundError
from ._kubernetes import (
    ResourceNotUniqueError as ResourceNotUniqueError,
)
from ._kubernetes import (
    UnprocessibleEntityError as UnprocessibleEntityError,
)
from ._kubernetes import DynamicApiError as DynamicApiError


class InvalidParameter(Exception):
    pass


class EventTimeoutError(TimeoutError):
    """Used when a waiting for an event times out."""

    def __init__(self, *args, last):
        super().__init__(*args)
        self.last = last
