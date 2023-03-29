from kubernetes.dynamic.exceptions import ConflictError as ConflictError
from kubernetes.dynamic.exceptions import NotFoundError as NotFoundError
from kubernetes.dynamic.exceptions import (
    ResourceNotUniqueError as ResourceNotUniqueError,
)
from kubernetes.dynamic.exceptions import (
    UnprocessibleEntityError as UnprocessibleEntityError,
)


class InvalidParameter(Exception):
    pass
