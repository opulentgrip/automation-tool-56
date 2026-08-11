from typing import List, Dict, Any


def filter_dict_keys(data: Dict[str, Any], keys: List[str]) -> Dict[str, Any]:
    """
    Filters a dictionary, returning a new dictionary with only the specified keys.

    Args:
        data (Dict[str, Any]): The original dictionary to filter.
        keys (List[str]): A list of keys to retain in the new dictionary.

    Returns:
        Dict[str, Any]: A new dictionary containing only the specified keys.
    """
    return {key: data[key] for key in keys if key in data}


def merge_dicts(dict1: Dict[str, Any], dict2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Merges two dictionaries into one. If a key exists in both,
    the value from the second dictionary will be used.

    Args:
        dict1 (Dict[str, Any]): The first dictionary.
        dict2 (Dict[str, Any]): The second dictionary.

    Returns:
        Dict[str, Any]: A new dictionary with merged key-value pairs.
    """
    merged = dict1.copy()
    merged.update(dict2)
    return merged


def get_nested_value(data: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
    """
    Retrieves a value from a nested dictionary using a list of keys.
    If any key is not found, returns the specified default value.

    Args:
        data (Dict[str, Any]): The nested dictionary.
        keys (List[str]): A list of keys to traverse.
        default (Any): The value to return if the keys are not found.

    Returns:
        Any: The retrieved value or the default value.
    """
    for key in keys:
        if isinstance(data, dict) and key in data:
            data = data[key]
        else:
            return default
    return data
