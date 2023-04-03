import http
from enum import Enum
from typing import Any, Dict, Generic, TypeVar

import pydantic
from urllib3 import HTTPResponse

from kubernetes_dynamic.exceptions import ApiException, api_exception
from kubernetes_dynamic.models.resource_value import ResourceValue

HTTP_STATUS_GONE = http.HTTPStatus.GONE


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
    ERROR = "ERROR"


class Event(ResourceValue, Generic[R]):
    """Kubernetes event object."""

    type: EventType
    object: R
    raw_object: Dict[str, Any]

    @pydantic.root_validator(pre=True)
    def build_extra(cls, values: Dict[str, Any]) -> Dict[str, Any]:  # noqa: B902, N805
        """Automatically add raw_object from object."""
        if "raw_object" not in values:
            values["raw_object"] = values["object"] if isinstance(values["object"], dict) else values["object"].dict()
        return values


class Watch(object):
    def __init__(self, api_client, return_type=None):
        from kubernetes_dynamic.models.resource_item import ResourceItem

        self._return_type = return_type or ResourceItem
        self._stop = False
        self._api_client = api_client
        self.resource_version = None
        self.timeout_seconds = None

    def stop(self):
        self._stop = True

    def stream(
        self,
        func,
        *args,
        resource_version=None,
        watch=True,
        _preload_content=False,
        timeout_seconds=None,
        **kwargs,
    ):
        self._stop = False
        self.resource_version = resource_version or self.resource_version
        self.timeout_seconds = timeout_seconds
        retry_after_410 = False
        while not self._stop:
            resp: HTTPResponse = func(
                *args,
                resource_version=self.resource_version,
                watch=watch,
                _preload_content=_preload_content,
                timeout_seconds=timeout_seconds or 5,
                **kwargs,
            )
            try:
                yield from self._parse_response_iter(resp)
            except ApiException as e:
                if e.status == 410 and not retry_after_410:
                    self.resource_version = func(*args, **kwargs).metadata.resourceVersion
                    retry_after_410 = True
                    continue
                raise api_exception(e) from e
            finally:
                resp.close()
                resp.release_conn()
                if timeout_seconds or self.resource_version is None:
                    self._stop = True

    def _parse_response_iter(self, resp: HTTPResponse):
        for line in resp:
            event = pydantic.parse_raw_as(Event, line)
            if event.type == EventType.ERROR:
                raise ApiException(event.object.code)

            event.object = self._return_type(event.object)
            self.resource_version = event.raw_object.get("metadata", {}).get("resourceVersion")
            yield event

            if self._stop:
                break
