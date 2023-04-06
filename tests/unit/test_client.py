from typing import Any
from unittest.mock import MagicMock

import pytest

from kubernetes_dynamic._kubernetes import ResourceApi
from kubernetes_dynamic.client import K8sClient
from kubernetes_dynamic.exceptions import InvalidParameter
from kubernetes_dynamic.formatters import format_selector
from kubernetes_dynamic.kube.exceptions import (
    ConfigException,
    ResourceNotUniqueError,
)
from kubernetes_dynamic.models.pod import V1Pod


def resource_api(namespaced=True, obj_type=None):
    return MagicMock(namespaced=namespaced, _resource_type=obj_type)


def fake_pod():
    return V1Pod.parse_obj({"kind": "Pod", "apiVersion": "v1"})


def fake_pods():
    return [V1Pod.parse_obj({"kind": "Pod", "apiVersion": "v1", "metadata": {"name": "pod-name"}})]


def test_k8s_client_init_incluster(mock_load_incluster: MagicMock):
    mock_load_incluster.side_effect = None
    cl = K8sClient()
    assert cl.in_cluster


def test_k8s_client_init_not_incluster(mock_load_incluster: MagicMock):
    mock_load_incluster.side_effect = ConfigException
    cl = K8sClient()
    assert not cl.in_cluster


def test_k8s_find_context():
    loader = MagicMock()
    contexts = loader.list_contexts
    contexts.return_value = [
        [],
        {"notcontext": {"cluster": "cluster_name_0"}},
        {"name": "context_name_1", "context": {"cluster": "cluster_name_1"}},
        {"name": "context_name_2", "context": {"cluster": "cluster_name_2"}},
    ]
    assert K8sClient.find_context(None, loader) is None
    assert K8sClient.find_context("cluster_name_1", loader) == "context_name_1"
    assert K8sClient.find_context("context_name_2", loader) == "context_name_2"
    with pytest.raises(RuntimeError):
        K8sClient.find_context("cluster_name", loader)


@pytest.mark.parametrize(
    "name, object_type, api_version, kind, filter",
    [
        ("pods", V1Pod, "v1", "Pod", {}),
        (None, V1Pod, "v1", "Pod", {}),
        (None, V1Pod, None, "Pod", {}),
        (None, V1Pod, "v1", None, {}),
        (None, None, "v1", "Pod", {}),
        ("pods", None, "v1", None, {}),
        ("pods", None, "v1", None, {"something": "value"}),
    ],
)
def test_k8s_client_get_api(
    name: str,
    object_type: Any,
    api_version: str,
    kind: str,
    filter: dict,
    mock_resources: MagicMock,
):
    mock_resources.get.return_value = MagicMock(kind="Pod", api_version="v1")
    cl = K8sClient()
    api = cl.get_api(name=name, object_type=object_type, api_version=api_version, kind=kind, **filter)
    filter_dict = filter
    if api_version:
        filter_dict["api_version"] = api_version
    if kind:
        filter_dict["kind"] = kind
    if name:
        filter_dict["name"] = name
    assert api == mock_resources.get.return_value
    assert api.resource_type == V1Pod
    mock_resources.get.assert_called_with(**filter_dict)


@pytest.mark.parametrize(
    "name, object_type, api_version, kind, filter",
    [
        ("pods", V1Pod, "v1", "Pod", {}),
        (None, V1Pod, "v1", "Pod", {}),
        (None, V1Pod, None, "Pod", {}),
        (None, V1Pod, "v1", None, {}),
        (None, None, "v1", "Pod", {}),
        ("pods", None, "v1", None, {}),
    ],
)
def test_k8s_client_get_api_not_unique(
    name: str,
    object_type: Any,
    api_version: str,
    kind: str,
    filter: dict,
    mock_resources: MagicMock,
):
    mock_resources.get.side_effect = ResourceNotUniqueError
    mock_resources.search.return_value = [
        MagicMock(kind="Pod", api_version="v2", preferred=False),
        MagicMock(kind="Pod", api_version="v1", preferred=True),
        MagicMock(kind="Pod", api_version="v1", preferred=True, spec=ResourceApi),
        MagicMock(kind="Pod", api_version="v4", preferred=False),
    ]
    cl = K8sClient()
    api = cl.get_api(name=name, object_type=object_type, api_version=api_version, kind=kind, **filter)
    filter_dict = filter
    if api_version:
        filter_dict["api_version"] = api_version
    if kind:
        filter_dict["kind"] = kind
    if name:
        filter_dict["name"] = name
    assert api == mock_resources.search.return_value[2]
    assert api.resource_type == V1Pod
    mock_resources.search.assert_called_with(**filter_dict)
    mock_resources.get.assert_called_with(**filter_dict)


def test_k8s_client_getattr(mock_resources: MagicMock):
    mock_resources.get.return_value = MagicMock(kind="Pod", api_version="v1")
    cl = K8sClient()
    assert cl.pods == mock_resources.get.return_value

    with pytest.raises(AttributeError):
        cl.__notexisting


@pytest.mark.parametrize(
    "selector, output",
    [
        ["string", "string"],
        [["label1", "label2"], "label1,label2"],
        [("label1", "label2"), "label1,label2"],
        [{"key": "string"}, "key=string"],
        [{"!key": "string"}, "key!=string"],
        [{"key": ["val1", "val2"]}, "key in (val1,val2)"],
        [{"!key": ["val1", "val2"]}, "key notin (val1,val2)"],
        [{"key": True}, "key"],
        [{"!key": None}, "!key"],
        [{"!k1": None, "k2": True, "k3": ["v1", "v2"]}, "!k1,k2,k3 in (v1,v2)"],
    ],
)
def test_k8s_client_format_selector(selector, output: str):
    """Test label selector formatting."""
    assert format_selector(selector) == output


def test_k8s_client_stream():
    method = MagicMock()
    method.return_value.read_all.return_value = "data"
    assert K8sClient().stream(method, "name", "namespace") == "data"


@pytest.mark.parametrize(
    "namespace, file_path, data, error, exc",
    [
        ("namespace", "file/path", {}, "mutually exclusive", InvalidParameter),
        ("namespace", "file/path", {"data": ""}, "mutually exclusive", InvalidParameter),
        ("namespace", None, None, "must be provided", InvalidParameter),
        ("namespace", "file/path", None, "file/path", FileNotFoundError),
    ],
)
def test_k8s_client_apply_errors(namespace, file_path, data, error, exc, mocker):
    path_mock = mocker.patch("kubernetes_dynamic.client.Path")
    path_mock.return_value.exists.return_value = False
    with pytest.raises(exc, match=error):
        K8sClient().apply(namespace=namespace, file_path=file_path, data=data)


def test_k8s_client_apply_empty(mocker):
    path_mock = mocker.patch("kubernetes_dynamic.client.Path")
    path_mock.return_value.exists.return_value = True
    mocker.patch("kubernetes_dynamic.client.open")
    yaml_mock = mocker.patch("kubernetes_dynamic.client.yaml")
    yaml_mock.full_load_all.return_value = []
    assert K8sClient().apply(namespace="namespace", file_path="file/path") == []


def test_k8s_client_apply(mocker, mock_resources):
    pod_api = MagicMock(kind="Pod", api_version="v1")
    mock_resources.get.return_value = pod_api
    path_mock = mocker.patch("kubernetes_dynamic.client.Path")
    path_mock.return_value.exists.return_value = True
    mocker.patch("kubernetes_dynamic.client.open")
    yaml_mock = mocker.patch("kubernetes_dynamic.client.yaml")
    yaml_mock.full_load_all.return_value = []
    item = {"kind": "Pod", "apiVersion": "v1", "metadata": {"name": "pod-name"}}
    expected = MagicMock()

    pod_api.apply.return_value = expected

    cl = K8sClient()
    cl.config.namespace = "my_namespace"
    assert cl.apply(data=item) == [expected]
