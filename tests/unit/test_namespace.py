from unittest.mock import MagicMock

from kubernetes_dynamic.kube.exceptions import ConflictError
from kubernetes_dynamic.models.namespace import V1Namespace


def test_namespace_init():
    pod = V1Namespace.parse_obj(dict(metadata={"name": "my_namespace"}))
    assert pod.metadata.name == "my_namespace"


def test_namespace_ensure(mock_client):
    mock_client.get_api.return_value.create.return_value = V1Namespace.parse_obj(
        dict(metadata={"name": "my_namespace"})
    )
    namespace = V1Namespace.ensure("my_namespace")
    assert namespace.metadata.name == "my_namespace"


def test_namespace_ensure_conflict(mock_client):
    mock_client.get_api.return_value.create.side_effect = ConflictError(MagicMock(name="my_namespace"))
    mock_client.get_api.return_value.get.return_value = V1Namespace.parse_obj(dict(metadata={"name": "my_namespace"}))
    namespace = V1Namespace.ensure("my_namespace")
    assert namespace.metadata.name == "my_namespace"


def test_namespace_annotate(mock_client):
    namespace = V1Namespace.parse_obj(dict(metadata={"name": "my_namespace"}))
    mock_client.get_api.return_value.get.return_value = V1Namespace.parse_obj(
        dict(metadata={"name": "my_namespace", "annotations": {"something": "1"}})
    )
    mock_client.get_api.return_value.patch.return_value = V1Namespace.parse_obj(
        dict(metadata={"name": "my_namespace", "annotations": {"something": "1", "something_2": "2"}})
    )
    namespace.annotate({"something_2": "2"})
    assert namespace.metadata.annotations == {"something": "1", "something_2": "2"}
    mock_client.get_api.return_value.patch.assert_called()
