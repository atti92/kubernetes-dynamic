from unittest.mock import MagicMock

import pytest

from kubernetes_dynamic.kube.exceptions import NotFoundError
from kubernetes_dynamic.models.resource_item import CheckResult, ResourceItem


def test_resource_init_dict():
    item = ResourceItem(dict(key1="val1", key2={"subkey1": 3}, key3=[{"subl1": 4}]))
    assert item.key1 == "val1"
    assert item.key2.subkey1 == 3
    assert item.key3[0].subl1 == 4
    assert item.kind == ""
    assert item.apiVersion == ""


def test_resource_api(mock_client):
    """Resource API test."""
    mock_client.get_api.return_value = MagicMock(api_version="v1", kind="Kind")
    item = ResourceItem(dict(apiVersion="v1", kind="Kind", key1="val1", key2={"subkey1": 3}, key3=[{"subl1": 4}]))
    assert item.api is item.api


def test_resource_refresh(mock_client):
    item = ResourceItem(metadata={"name": "name", "namespace": "namespace"})

    mock_client.get_api.return_value.get.return_value = {"metadata": {"name": "name", "namespace": "namespace"}}
    assert item.refresh_() == item

    mock_client.get_api.return_value.get.return_value = None
    with pytest.raises(NotFoundError):
        item.refresh_()


def test_resource_is_ready(mock_client, mocker):
    is_ready_mock = mocker.patch("kubernetes_dynamic.models.resource_item.ResourceItem.check_object_is_ready")
    item = ResourceItem(metadata={"name": "name", "namespace": "namespace"})

    assert item.is_ready() == is_ready_mock.return_value
    mock_client.get_api.return_value.get.assert_not_called()
    assert item.is_ready(refresh=True) == is_ready_mock.return_value
    mock_client.get_api.return_value.get.assert_called()


def test_resource_delete(mock_client):
    item = ResourceItem(metadata={"name": "name", "namespace": "namespace"})
    assert item.delete_() == mock_client.get_api.return_value.delete.return_value
    mock_client.get_api.return_value.delete.assert_called()


@pytest.mark.parametrize(
    "conditions, result",
    [
        ([], CheckResult(False, "No conditions found on Kind name.")),
        (
            [{"status": "False"}, {"status": "True"}],
            CheckResult(False, "Condition not true on Kind name : ResourceValue:\n  status: 'False'\n."),
        ),
        (
            [{"status": "True"}, {"status": "True"}],
            CheckResult(True, "All conditions true on Kind name."),
        ),
    ],
)
def test_check_object_conditions(conditions, result):
    item = ResourceItem(
        dict(
            kind="Kind",
            metadata={"name": "name", "namespace": "namespace"},
            status={"conditions": conditions},
        )
    )
    res = ResourceItem.check_object_conditions(item)
    assert res == result
    assert bool(res) == result.state
    assert res == result.state


@pytest.mark.parametrize(
    "status, result",
    [
        ({}, CheckResult(True, "All 0 replicas ready on Kind name.")),
        (
            {"readyReplicas": 0, "replicas": 0},
            CheckResult(True, "All 0 replicas ready on Kind name."),
        ),
        (
            {"readyReplicas": 0, "replicas": 1},
            CheckResult(
                False,
                "Kind name only have 0 ready " "replicas out of required 1.",
            ),
        ),
        (
            {"readyReplicas": 1, "replicas": 1},
            CheckResult(True, "All 1 replicas ready on Kind name."),
        ),
    ],
)
def test_check_replicas_ready(status, result):
    item = ResourceItem(
        dict(
            kind="Kind",
            metadata={"name": "name", "namespace": "namespace"},
            status=status,
        )
    )
    res = ResourceItem.check_replicas_ready(item)
    assert res == result
    assert bool(res) == result.state
    assert res == result.state


def test_check_object_is_ready_no():
    item = MagicMock(status=None)
    assert ResourceItem.check_object_is_ready(item) == CheckResult(False, "Object has no status description.")


def test_check_object_is_ready_replicas(mocker):
    mock_replicas = mocker.patch("kubernetes_dynamic.models.resource_item.ResourceItem.check_replicas_ready")
    item = ResourceItem(
        dict(
            kind="Kind",
            metadata={"name": "name", "namespace": "namespace"},
            status={"replicas": 1},
        )
    )
    assert ResourceItem.check_object_is_ready(item) == mock_replicas.return_value


def test_check_object_is_ready_conditions(mocker):
    mock_conditions = mocker.patch("kubernetes_dynamic.models.resource_item.ResourceItem.check_object_conditions")
    item = ResourceItem(
        dict(
            kind="Kind",
            metadata={"name": "name", "namespace": "namespace"},
            status={"conditions": {"status": "True"}},
        )
    )
    assert ResourceItem.check_object_is_ready(item) == mock_conditions.return_value
