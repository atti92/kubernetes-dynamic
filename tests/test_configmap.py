from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from kubernetes_dynamic.models.configmap import V1ConfigMap


def test_configmap_init():
    pod = V1ConfigMap.parse_obj(dict(metadata={"name": "my_configmap"}))
    assert pod.metadata.name == "my_configmap"


@pytest.mark.parametrize(
    "mimetype, read, data, binary_data",
    [
        ("text", "data", {"file_path": "data"}, {}),
        (None, b"\a4", {}, {"file_path": "BzQ="}),
    ],
)
def test_configmap_from_path_file(mimetype, read, data, binary_data, mocker: MockerFixture):
    path_mock = mocker.patch("kubernetes_dynamic.models.configmap.Path").return_value
    mimetypes_mock = mocker.patch("kubernetes_dynamic.models.configmap.mimetypes")
    path_mock.is_dir.return_value = False
    path_mock.open.return_value.__enter__.return_value.read.return_value = read
    path_mock.name = "file_path"
    mimetypes_mock.guess_type.return_value = (mimetype, None)
    configmap = V1ConfigMap.from_path("cm-name", "cm-namespace", "file_path")
    assert configmap.data == data
    assert configmap.binaryData == binary_data


def test_configmap_from_path_dir(mocker: MockerFixture):
    path_mock = mocker.patch("kubernetes_dynamic.models.configmap.Path").return_value
    path_data_mock = mocker.patch("kubernetes_dynamic.models.configmap.V1ConfigMap._path_to_data_item")
    path_mock.is_dir.return_value = True
    file_1 = MagicMock(is_dir=lambda: False, **{"name": "file_1"})
    file_2 = MagicMock(is_dir=lambda: False, **{"name": "file_2"})
    file_3 = MagicMock(is_dir=lambda: True, **{"name": "file_3"})
    path_mock.iterdir.return_value = [file_1, file_2, file_3]
    path_data_mock.side_effect = [
        {"data": {"file_1": "data"}, "binaryData": {}},
        {"data": {}, "binaryData": {"file_2": "BzQ="}},
    ]
    configmap = V1ConfigMap.from_path("cm-name", "cm-namespace", "file_path")
    assert configmap.data == {"file_1": "data"}
    assert configmap.binaryData == {"file_2": "BzQ="}
