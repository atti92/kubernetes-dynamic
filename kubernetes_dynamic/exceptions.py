__all__ = [
    "ApiException",
    "DynamicApiError",
    "ResourceNotFoundError",
    "ResourceNotUniqueError",
    "KubernetesValidateMissing",
    "BadRequestError",
    "UnauthorizedError",
    "ForbiddenError",
    "NotFoundError",
    "MethodNotAllowedError",
    "ConflictError",
    "GoneError",
    "UnprocessibleEntityError",
    "TooManyRequestsError",
    "InternalServerError",
    "ServiceUnavailableError",
    "ServerTimeoutError",
    "ConfigException",
    "api_exception",
]


from kubernetes_dynamic.kube.exceptions import (
    BadRequestError,
    ConfigException,
    ConflictError,
    DynamicApiError,
    ForbiddenError,
    GoneError,
    InternalServerError,
    KubernetesValidateMissing,
    MethodNotAllowedError,
    NotFoundError,
    ResourceNotFoundError,
    ResourceNotUniqueError,
    ServerTimeoutError,
    ServiceUnavailableError,
    TooManyRequestsError,
    UnauthorizedError,
    UnprocessibleEntityError,
    api_exception,
)
from kubernetes_dynamic.openapi_client.exceptions import ApiException


class InvalidParameter(Exception):
    pass


class EventTimeoutError(TimeoutError):
    """Used when a waiting for an event times out."""

    def __init__(self, *args, last):
        super().__init__(*args)
        self.last = last
