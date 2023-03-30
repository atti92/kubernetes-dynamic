import pytest
from pytest_mock import MockerFixture

import kubernetes_dynamic._kubernetes


@pytest.fixture(autouse=True)
def mock_kubernetes(mocker: MockerFixture):
    def _init(*args, **kwargs):
        return None

    mocker.patch.object(kubernetes_dynamic._kubernetes.dynamic.DynamicClient, "__init__", _init)
    mocker.patch.object(kubernetes_dynamic._kubernetes.dynamic.DynamicClient, "get", autospec=True)
    mocker.patch.object(kubernetes_dynamic._kubernetes.dynamic.DynamicClient, "create", autospec=True)
    mocker.patch.object(kubernetes_dynamic._kubernetes.dynamic.DynamicClient, "delete", autospec=True)
    mocker.patch.object(kubernetes_dynamic._kubernetes.dynamic.DynamicClient, "replace", autospec=True)
    mocker.patch.object(kubernetes_dynamic._kubernetes.dynamic.DynamicClient, "patch", autospec=True)
    mocker.patch.object(kubernetes_dynamic._kubernetes.dynamic.DynamicClient, "watch", autospec=True)
    mocker.patch.object(kubernetes_dynamic._kubernetes.dynamic.DynamicClient, "server_side_apply", autospec=True)
    mocker.patch.object(kubernetes_dynamic._kubernetes, "ApiClient", autospec=True)
    mocker.patch.object(kubernetes_dynamic._kubernetes.InClusterConfigLoader, "__init__", _init)
    mocker.patch.object(kubernetes_dynamic._kubernetes.InClusterConfigLoader, "load_and_set", autospec=True)
    mocker.patch.object(kubernetes_dynamic._kubernetes.KubeConfigLoader, "__init__", _init)
    mocker.patch.object(kubernetes_dynamic._kubernetes.KubeConfigLoader, "load_and_set", autospec=True)
    mocker.patch.object(kubernetes_dynamic._kubernetes.KubeConfigLoader, "set_active_context", autospec=True)
    mocker.patch.object(kubernetes_dynamic._kubernetes, "_get_kube_config_loader", autospec=True)
    mocker.patch.object(kubernetes_dynamic._kubernetes, "Watch", autospec=True)
    return kubernetes_dynamic._kubernetes


@pytest.fixture
def mock_load_incluster(mock_kubernetes):
    return mock_kubernetes.InClusterConfigLoader.load_and_set


@pytest.fixture
def mock_resources(mocker):
    return mocker.patch("kubernetes_dynamic.client.K8sClient.resources")


@pytest.fixture
def mock_dclient(mock_kubernetes):
    return mock_kubernetes.dynamic.DynamicClient


@pytest.fixture
def mock_client(mocker: MockerFixture):
    return mocker.patch("kubernetes_dynamic.client.K8sClient").return_value
