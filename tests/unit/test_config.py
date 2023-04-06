from unittest.mock import MagicMock

from kubernetes_dynamic.config import MutedSecretsSettingsSource


def test_pydantic_mute_no_secrets():
    source = MagicMock(secrets_dir=None)
    settings = MagicMock()
    settings_source = MutedSecretsSettingsSource(source)
    assert settings_source(settings) == {}


def test_pydantic_mute_path(mocker):
    mocker.patch("kubernetes_dynamic.config.Path").return_value.expanduser.return_value.exists.return_value = False
    source = MagicMock(secrets_dir="test/path")
    settings = MagicMock()
    settings_source = MutedSecretsSettingsSource(source)
    assert settings_source(settings) == {}


def test_pydantic_mute_full(mocker):
    mocker.patch("kubernetes_dynamic.config.Path")
    source = MagicMock(secrets_dir="test/path")
    settings = MagicMock()
    settings_source = MutedSecretsSettingsSource(source)
    assert settings_source(settings) == source.return_value
