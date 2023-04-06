from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

import kubernetes_dynamic._kubernetes


@pytest.fixture(autouse=True)
def mock_kubernetes(mocker: MockerFixture):
    mocker.patch("kubernetes_dynamic._kubernetes.LazyDiscoverer")
    api_client = mocker.patch.object(kubernetes_dynamic._kubernetes, "ApiClient", autospec=True)
    api_client.return_value.configuration = MagicMock()
    mocker.patch.object(kubernetes_dynamic._kubernetes.InClusterConfigLoader, "__init__", return_value=None)
    mocker.patch.object(kubernetes_dynamic._kubernetes.InClusterConfigLoader, "load_and_set", autospec=True)
    mocker.patch.object(kubernetes_dynamic._kubernetes.KubeConfigLoader, "__init__", return_value=None)
    mocker.patch.object(kubernetes_dynamic._kubernetes.KubeConfigLoader, "load_and_set", autospec=True)
    mocker.patch.object(kubernetes_dynamic._kubernetes.KubeConfigLoader, "set_active_context", autospec=True)
    mocker.patch.object(kubernetes_dynamic._kubernetes, "_get_kube_config_loader", autospec=True)
    return kubernetes_dynamic._kubernetes


@pytest.fixture
def mock_load_incluster(mock_kubernetes):
    return mock_kubernetes.InClusterConfigLoader.load_and_set


@pytest.fixture
def mock_resources(mocker):
    return mocker.patch("kubernetes_dynamic.client.K8sClient.resources")


@pytest.fixture
def mock_request(mocker):
    return mocker.patch("kubernetes_dynamic.client.K8sClient.request")


@pytest.fixture
def mock_client(mocker: MockerFixture):
    return mocker.patch("kubernetes_dynamic.client.K8sClient").return_value
