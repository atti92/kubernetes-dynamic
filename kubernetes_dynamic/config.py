from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

from . import _kubernetes
import pydantic


class MutedSecretsSettingsSource:
    """Disable warning when secrets dir does not exist."""

    def __init__(self, source: pydantic.env_settings.SecretsSettingsSource):
        self.source = source

    def __call__(self, settings: pydantic.BaseSettings):
        secrets: Dict[str, Optional[str]] = {}

        if self.source.secrets_dir is None:
            return secrets

        secrets_path = Path(self.source.secrets_dir).expanduser()

        if not secrets_path.exists():
            return secrets
        return self.source(settings)


class K8sConfig(pydantic.BaseSettings):
    """Kubernetes configuration options."""

    configuration: Optional[_kubernetes.Configuration] = None
    context: str = pydantic.Field(default="", env="KUBE_CONTEXT")
    namespace: str = pydantic.Field(default="default", env=["NAMESPACE", "KUBE_NAMESPACE"])
    connection_timeout: int = pydantic.Field(default=10, env="KUBERNETES_CONNECTION_TIMEOUT")
    read_timeout: int = pydantic.Field(default=30, env="KUBERNETES_READ_TIMEOUT")

    class Config:  # noqa: D106
        arbitrary_types_allowed = True
        secrets_dir = "/run/secrets/kubernetes.io/serviceaccount"

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            """Configure settings priority in return order."""
            return init_settings, env_settings, MutedSecretsSettingsSource(file_secret_settings)
