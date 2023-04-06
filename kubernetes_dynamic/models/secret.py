from __future__ import annotations

import base64
from typing import Dict, List, Tuple, Union, overload

from pydantic import Field, PrivateAttr
from typing_extensions import Literal

from .resource_item import ResourceItem


class V1Secret(ResourceItem):
    """Extended Kubernetes Secret object."""

    data: Dict[str, str] = Field(default_factory=dict)
    immutable: bool = False
    stringData: Dict[str, str] = Field(default_factory=dict)
    type: str = "Opaque"

    _required_keys: Union[tuple, List] = PrivateAttr(default_factory=tuple)

    def __init__(
        self,
        *args,
        required_keys: Union[tuple, List] = (),
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._required_keys = required_keys

    def exists(self) -> bool:
        """Checks if the secret exists in Kubernetes."""
        return self.read_() is not None

    def validate_keys(self) -> Tuple[bool, bool, list]:
        """Validates a secret exists and has the correct format."""
        secret = self.read_()
        is_valid = True
        missing_data_keys = []

        if secret is None:
            return (False, False, missing_data_keys)

        if self.type is not None and secret.type != self.type:
            is_valid = False

        missing_data_keys = self.get_missing_keys(secret.data)
        if missing_data_keys:
            is_valid = False

        return (True, is_valid, missing_data_keys)

    def get_missing_keys(self, data) -> List[str]:
        """Returns required keys that are missing from the secret data."""
        missing_keys = []
        if not data:
            missing_keys = list(self._required_keys)
        else:
            for k in self._required_keys:
                if k not in data:
                    missing_keys.append(k)
        return missing_keys

    @overload
    def decode(self, key: str, encoding: Literal["bytes"] | Literal[""]) -> bytes:
        ...  # pragma: no cover

    @overload
    def decode(self, key: str, encoding: str = "utf-8") -> str:
        ...  # pragma: no cover

    def decode(self, key: str, encoding: str = "utf-8") -> str | bytes:
        """Return decoded secret key."""
        try:
            data = base64.b64decode(self.data[key])
            if not encoding or encoding == "bytes":
                return data
            return data.decode(encoding)
        except KeyError:
            return ""

    def decode_all(self) -> dict[str, bytes]:
        """Return decoded secret data."""
        decoded_data = {}
        for key in self.data:
            decoded_data[key] = self.decode(key, encoding="bytes")
        return decoded_data

    def set(self, key: str, value: str | bytes, encoding: str = "utf-8"):
        """Add an item to the secret and encode it."""
        if isinstance(value, str):
            value = value.encode(encoding)
        self.data[key] = base64.b64encode(value).decode()
        return self
