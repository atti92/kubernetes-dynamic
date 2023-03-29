from __future__ import annotations

from typing import Any, Dict, Optional

import pydantic
import yaml


class AllOptional(pydantic.main.ModelMetaclass):
    """Extends pydantic model params with Optional flag."""

    def __new__(cls, name, bases, namespaces, **kwargs):
        def _is_change_needed(key):
            if key in namespaces:
                return False
            if isinstance(namespaces["__annotations__"][key], str) and namespaces["__annotations__"][key].startswith(
                "Optional"
            ):
                return False
            return True

        annotations = namespaces.get("__annotations__", {})
        namespaces["__annotations__"] = {
            key: Optional[value] if _is_change_needed(key) else value for key, value in annotations.items()
        }
        return super().__new__(cls, name, bases, namespaces, **kwargs)


class ResourceValue(pydantic.BaseModel, metaclass=AllOptional):
    """Every kubernetes field with dictionary like format."""

    class Config:
        """Pydantic config class."""

        extra = "allow"
        arbitrary_types_allowed = True

    @pydantic.root_validator(pre=True)
    def build_extra(cls, values: Dict[str, Any]) -> Dict[str, Any]:  # noqa: B902, N805
        """Automatically convert extra items to ResourceFields."""
        field_names = {field.alias for field in cls.__fields__.values()}

        def convert(item: Any):
            if isinstance(item, dict):
                return ResourceValue(**item)
            if isinstance(item, list):
                return [convert(it) for it in item]
            return item

        for name, value in values.items():
            if name in field_names:
                continue
            values[name] = convert(value)
        return values

    def _update_attrs(self, data: dict | ResourceValue):
        data = self.validate(data)
        for key in data.__fields__:
            setattr(self, key, getattr(data, key))
        return self

    def __repr__(self):
        return "{}:\n  {}".format(self.__class__.__name__, "  ".join(yaml.safe_dump(self.dict()).splitlines(True)))

    def __getattribute__(self, name: str) -> Any:
        return super().__getattribute__(name)

    def __getattr__(self, name: str):
        return None

    def __getitem__(self, name):
        return getattr(self, name)

    def __setitem__(self, name, value):
        setattr(self, name, value)

    def to_dict(self):
        """Convert to dict."""
        return self.dict()

    def to_str(self):
        """Get a yaml string representation."""
        return repr(self)

    def get(self, name, default=None):
        """Same as dict.get."""
        return self[name] or default
