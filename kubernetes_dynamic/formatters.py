
from typing import Union

SelectorTypes = Union[None, str, dict, list, tuple]

def _format_dict_selector(selector: dict):
    items = []
    for key, value in selector.items():
        exists = True
        if key.startswith("!"):
            exists = False
            key = key[1:]
        if isinstance(value, (tuple, list)):
            items.append(f"{key} {'in' if exists else 'notin'} ({format_selector(value)})")
        elif isinstance(value, str):
            items.append(f"{key}{'!' if not exists else ''}={value}")
        elif not exists or value is False:
            items.append(f"!{key}")
        else:
            items.append(key)
    return format_selector(items)

def format_selector(selector: SelectorTypes):
    """Format kubernetes selector.

    Args:
        selector: The selector object to convert.
            - string: no conversion done.
            - list, tuple: the object is concatenated by `,`.
            - dict:
                - key: string           -> key=string             # key equals string
                - !key: string          -> key!=string            # key not equals string
                - key: [val1, val2]     -> key in (val1, val2)    # key is val1 OR val2
                - !key: [val1, val2]    -> key notin (val1, val2) # key is NOT val1 AND NOT val2
                - key: True             -> key                    # key exists
                - key: False            -> !key                   # key NOT exists
                - !key: None            -> !key                   # key NOT exists

    Returns:
        Kubernetes compatible string selector
    """
    if isinstance(selector, (list, tuple)):
        return ",".join(selector)
    if isinstance(selector, dict):
        return _format_dict_selector(selector)
    return selector
