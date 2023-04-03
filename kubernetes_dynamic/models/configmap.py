from __future__ import annotations

import base64
import mimetypes
from pathlib import Path
from typing import Dict, cast

from pydantic import Field

from kubernetes_dynamic.models.common import V1ObjectMeta

from .resource_item import ResourceItem


class V1ConfigMap(ResourceItem):
    binaryData: Dict[str, str] = Field(default_factory=dict)
    data: Dict[str, str] = Field(default_factory=dict)
    immutable: bool = False

    @staticmethod
    def _path_to_data_item(file_path: str | Path):
        file_path = Path(file_path)
        mimetype = mimetypes.guess_type(str(file_path))[0]
        item = {"data": {}, "binaryData": {}}
        if mimetype and mimetype.startswith("text"):
            with file_path.open("rt") as f:
                item["data"] = {file_path.name: f.read()}
        else:
            with file_path.open("rb") as f:
                item["binaryData"] = {file_path.name: base64.b64encode(f.read()).decode()}
        return item

    @classmethod
    def from_path(cls, name: str, namespace: str, file_path: str | Path):
        """Instantiate a configmap from file."""
        file_path = Path(file_path)
        data = {}
        binary_data = {}
        items = [file_path] if not file_path.is_dir() else [path for path in file_path.iterdir() if not path.is_dir()]
        for item in items:
            item_data = V1ConfigMap._path_to_data_item(item)
            data.update(item_data["data"])
            binary_data.update(item_data["binaryData"])
        configmap = cls(
            metadata=cast(
                V1ObjectMeta,
                {
                    "name": name,
                    "namespace": namespace,
                },
            ),
            apiVersion="v1",
            kind="ConfigMap",
            data=data,
            binaryData=binary_data,
        )
        return configmap
