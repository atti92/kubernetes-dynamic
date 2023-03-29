from ._kubernetes import ConfigException as ConfigException
from ._kubernetes import ConflictError as ConflictError
from ._kubernetes import NotFoundError as NotFoundError
from ._kubernetes import (
    ResourceNotUniqueError as ResourceNotUniqueError,
)
from ._kubernetes import (
    UnprocessibleEntityError as UnprocessibleEntityError,
)


class InvalidParameter(Exception):
    pass
