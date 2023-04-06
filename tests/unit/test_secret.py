from unittest.mock import MagicMock

import pytest

from kubernetes_dynamic.models.secret import V1Secret


def test_secret_init():
    secret = V1Secret(metadata={"name": "my_secret"}, data={"key": "value"})
    assert secret.metadata.name == "my_secret"
    assert secret.data["key"] == "value"


def test_secret_exists(mock_client):
    secret = V1Secret(metadata={"name": "my_secret"})
    assert secret.exists()
    mock_client.get_api.return_value.get.return_value = None
    assert not secret.exists()


@pytest.mark.parametrize(
    "secret, expected",
    [
        (MagicMock(data={"key3": ""}, type="Opaque"), (True, False, ["key1", "key2"])),
        (MagicMock(data={}, type="Opaque"), (True, False, ["key1", "key2", "key3"])),
        (MagicMock(data={}, type="Other"), (True, False, ["key1", "key2", "key3"])),
        (None, (False, False, [])),
        (MagicMock(data={"key3": "", "key2": "", "key1": ""}, type="Opaque"), (True, True, [])),
    ],
)
def test_secret_validate_keys(secret, expected, mock_client):
    mock_client.get_api.return_value.get.return_value = secret
    secret = V1Secret(type="Opaque", metadata={"name": "my_secret"}, required_keys=("key1", "key2", "key3"))
    assert secret.validate_keys() == expected


def test_secret_decode():
    secret = V1Secret(metadata={"name": "my_secret"}, data={"key1": "dGVzdCBzdHJpbmc="})
    assert secret.decode("key1") == "test string"
    assert secret.decode("key_non") == ""


def test_secret_update_empty():
    secret = V1Secret(metadata={"name": "my_secret"})
    secret.set("key1", "test string")
    assert secret.data["key1"] == "dGVzdCBzdHJpbmc="


def test_secret_update_binary():
    secret = V1Secret(metadata={"name": "my_secret"})
    secret.set("key_binary", b"\a4")
    assert secret.data["key_binary"] == "BzQ="
    assert secret.decode("key_binary", "bytes") == b"\a4"
    assert secret.decode("key_binary", "") == b"\a4"


def test_secret_update_same_key():
    secret = V1Secret(metadata={"name": "my_secret"}, data={"key1": "dGVzdCBzdHJpbmc="})
    secret.set("key1", "test string 2")
    assert secret.data["key1"] == "dGVzdCBzdHJpbmcgMg=="


def test_secret_update_other_empty_key():
    secret = V1Secret(metadata={"name": "my_secret"}, data={"key1": "dGVzdCBzdHJpbmc="})
    secret.set("key2", "test string 2")
    assert secret.data["key1"] == "dGVzdCBzdHJpbmc="
    assert secret.data["key2"] == "dGVzdCBzdHJpbmcgMg=="


def test_secret_update_other_key():
    secret = V1Secret(
        metadata={"name": "my_secret"},
        data={"key1": "dGVzdCBzdHJpbmc=", "key2": "dGVzdCBzdHJpbmcgMg=="},
    )
    secret.set("key1", "other test string")
    assert secret.data["key1"] == "b3RoZXIgdGVzdCBzdHJpbmc="
    assert secret.data["key2"] == "dGVzdCBzdHJpbmcgMg=="
