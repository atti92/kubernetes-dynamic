from typing import Optional, Union

from kubernetes_dynamic.resource_value import ResourceValue


def test_resource_field_new():
    class ResourceFieldSample(ResourceValue):
        a: int
        b: "Optional[bool]"
        c: Optional[bool]

    assert ResourceFieldSample.__fields__["a"].annotation == Union[int, None]
    assert ResourceFieldSample.__fields__["b"].annotation == Union[bool, None]
    assert ResourceFieldSample.__fields__["c"].annotation == Union[bool, None]


def test_resource_field_init():
    item = ResourceValue(key1="val1", key2={"subkey1": 3}, key3=[{"subl1": 4}])
    assert item.key1 == "val1"
    assert isinstance(item.key2, ResourceValue)
    assert item.key2.subkey1 == 3
    assert isinstance(item.key3[0], ResourceValue)
    assert item.key3[0].subl1 == 4


def test_resource_dict_methods():
    item = ResourceValue(key1="val1", key2={"subkey1": 3}, key3=[{"subl1": 4}])
    assert item.to_dict() == dict(key1="val1", key2={"subkey1": 3}, key3=[{"subl1": 4}])
    assert repr(item) == item.to_str()
    assert item.get("key1") == "val1"
    assert item.get("key6") is None
    item["key5"] = "newval"
    assert item["key5"] == "newval"
