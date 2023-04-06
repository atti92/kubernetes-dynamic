from unittest.mock import MagicMock

import pydantic
import pytest

from kubernetes_dynamic.client import K8sClient
from kubernetes_dynamic.events import Event
from kubernetes_dynamic.kube.exceptions import NotFoundError
from kubernetes_dynamic.kube.resource_api import ResourceApi
from kubernetes_dynamic.models.pod import V1Pod
from kubernetes_dynamic.models.resource_value import ResourceValue


@pytest.fixture
def fake_api(mock_client: K8sClient):
    return ResourceApi(name="pods", kind="Pod", api_version="v1", prefix="", namespaced=True, client=mock_client)


def fake_pod():
    return V1Pod.parse_obj({"kind": "Pod", "apiVersion": "v1", "metadata": {"name": "pod-name"}})


def test_k8s_resource_get(fake_api: ResourceApi, mock_client: K8sClient):
    """Test get method."""
    mock_client.request.return_value = fake_pod()
    assert fake_api.get("name", "namespace") == fake_pod()

    mock_client.request.side_effect = NotFoundError(MagicMock())
    assert fake_api.get("name", "namespace") is None


def test_find(fake_api: ResourceApi, mock_client: K8sClient):
    """Test generic find method."""
    pods = [fake_pod()]
    mock_client.request.return_value = pods
    assert fake_api.find("pod-.*", "namespace") == pods

    mock_client.request.side_effect = [pods]
    assert fake_api.find("something.*", "namespace") == []


def test_k8s_client_get_clusterwide(fake_api: ResourceApi, mock_client: K8sClient):
    mock_client.request.return_value = fake_pod()
    fake_api.namespaced = False
    assert fake_api.get("name", "namespace") == fake_pod()


def test_k8s_client_get_kwarg_namespace(fake_api: ResourceApi, mock_client: K8sClient):
    mock_client.request.return_value = fake_pod()
    assert fake_api.get("name", namespace="namespace") == fake_pod()


def test_k8s_client_get_404(fake_api: ResourceApi, mock_client: K8sClient):
    mock_client.request.side_effect = (NotFoundError(fake_pod()),)
    assert fake_api.get("name", "namespace") is None


def test_k8s_client_create(fake_api: ResourceApi, mock_client: K8sClient):
    mock_client.request.return_value = fake_pod()
    assert fake_api.create(MagicMock(), "namespace") == fake_pod()


def test_k8s_client_delete(fake_api: ResourceApi, mock_client: K8sClient):
    mock_client.request.return_value = fake_pod()
    assert (
        fake_api.delete("name", "namespace", {}, label_selector="label_selector", field_selector="field_selector")
        == fake_pod()
    )


def test_k8s_client_replace(fake_api: ResourceApi, mock_client: K8sClient):
    mock_client.request.return_value = fake_pod()
    assert (
        fake_api.replace(
            MagicMock(),
            "name",
            "namespace",
        )
        == fake_pod()
    )


def test_k8s_client_patch(fake_api: ResourceApi, mock_client: K8sClient):
    mock_client.request.return_value = fake_pod()
    assert (
        fake_api.patch(
            MagicMock(),
            "name",
            "namespace",
        )
        == fake_pod()
    )


def test_k8s_client_server_side_apply(fake_api: ResourceApi, mock_client: K8sClient):
    mock_client.request.return_value = fake_pod()
    assert fake_api.server_side_apply(MagicMock(), "name", "namespace", True) == fake_pod()


def test_k8s_client_watch(fake_api: ResourceApi, mock_client: K8sClient):
    resp = MagicMock()
    resp.__iter__.return_value = [
        '{"type": "ADDED", "object": {"apiVersion": "v1", "kind": "A", "data": 1}}',
        '{"type": "DELETED", "object": {"apiVersion": "v1", "kind": "A", "data": 1}}',
        '{"type": "MODIFIED", "object": {"apiVersion": "v1", "kind": "A", "data": 1}}',
        '{"type": "ERROR", "object": {"apiVersion": "v1", "kind": "A", "data": 1}}',
    ]
    fake_api.resource_type = ResourceValue
    mock_client.request.return_value = resp
    for idx, item in enumerate(
        fake_api.watch(
            "namespace",
            "name",
            "label_selector",
            "field_selector",
            "resource_version",
            10,
            None,
        )
    ):
        assert item == pydantic.parse_raw_as(Event, resp.__iter__.return_value[idx])
        assert isinstance(item.object, ResourceValue)
        assert item.object.data == 1
