from __future__ import annotations

from typing import Any, Dict

import pydantic
import yaml


class ResourceValue(pydantic.BaseModel):
    """Every kubernetes field with dictionary like format."""

    class Config:
        """Pydantic config class."""

        extra = "allow"
        arbitrary_types_allowed = True
        use_enum_values = True

    def __init__(
        self,
        definition: dict[str, Any] | ResourceValue | None = None,
        **kwargs,
    ):
        final_def = ResourceValue.merge_definition_with_kwargs(definition, **kwargs)
        super().__init__(**final_def)

    @classmethod
    def merge_definition_with_kwargs(
        cls,
        definition: dict | ResourceValue | None = None,
        **kwargs,
    ) -> dict[str, Any]:
        final_def: dict = {}
        definition = definition or {}
        if isinstance(definition, dict):
            final_def = definition
        elif isinstance(definition, ResourceValue):
            final_def = definition.dict()  # type: ignore
        final_def.update(kwargs)
        return final_def

    @pydantic.root_validator(pre=True)
    def build_extra(cls, values: Dict[str, Any]) -> Dict[str, Any]:  # noqa: B902, N805
        """Automatically convert extra items to ResourceValues."""
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

    def __str__(self):
        return "{}:\n  {}".format(self.__class__.__name__, "  ".join(yaml.safe_dump(self.dict()).splitlines(True)))

    def __getattr__(self, name: str) -> Any:
        return None

    def __getitem__(self, name: str):
        return self.__dict__[name]

    def __setitem__(self, name: str, value: Any):
        setattr(self, name, value)

    def keys(self):
        return self.__dict__.keys()

    def to_dict(self):
        """Convert to dict."""
        return self.dict()

    def to_str(self):
        """Get a yaml string representation."""
        return str(self)

    def get(self, name: str, default: Any = None):
        """Same as dict.get."""
        return self.__dict__.get(name, default)

    def __contains__(self, m):
        return m in self.__dict__

    def pop(self, key, default):
        """Same as dict.pop."""
        return self.__dict__.pop(key, default)
