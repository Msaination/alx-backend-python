#!/usr/bin/env python3
"""
utils.py
Generic utilities for GitHub organization client.

Provides:
    - access_nested_map: safely access nested dictionaries
    - get_json: fetch JSON from a remote URL
    - memoize: decorator to cache method results

Usage:
    >>> from utils import access_nested_map, get_json, memoize
    >>> access_nested_map({"a": {"b": {"c": 42}}}, ["a", "b", "c"])
    42
"""

import requests
from functools import wraps
from typing import (
    Mapping,
    Sequence,
    Any,
    Dict,
    Callable,
)


__all__ = [
    "access_nested_map",
    "get_json",
    "memoize",
]


def access_nested_map(nested_map: Mapping[str, Any],
                      path: Sequence[str]) -> Any:
    """
    Access a value in a nested map using a sequence of keys.

    Parameters
    ----------
    nested_map : Mapping[str, Any]
        A nested dictionary-like object.
    path : Sequence[str]
        A sequence of keys representing the path to the desired value.

    Returns
    -------
    Any
        The value found at the specified path.

    Raises
    ------
    KeyError
        If any key in the path is not found.
    """
    for key in path:
        if not isinstance(nested_map, Mapping):
            raise KeyError(key)
        nested_map = nested_map[key]
    return nested_map


def get_json(url: str) -> Dict[str, Any]:
    """
    Fetch JSON content from a remote URL.

    Parameters
    ----------
    url : str
        The URL to fetch JSON from.

    Returns
    -------
    Dict[str, Any]
        Parsed JSON content from the response.

    Raises
    ------
    requests.RequestException
        If the request fails.
    """
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def memoize(fn: Callable) -> Callable:
    """
    Decorator to memoize a method's result.

    Parameters
    ----------
    fn : Callable
        The method to memoize.

    Returns
    -------
    Callable
        A property that caches the method's result.
    """
    attr_name = "_{}".format(fn.__name__)

    @wraps(fn)
    def memoized(self: Any) -> Any:
        """Wraps and caches the method result."""
        if not hasattr(self, attr_name):
            setattr(self, attr_name, fn(self))
        return getattr(self, attr_name)

    return property(memoized)


def main() -> None:
    """Run a simple demo of access_nested_map."""
    demo_map = {"a": {"b": {"c": 42}}}
    path = ["a", "b", "c"]
    print("Demo result:", access_nested_map(demo_map, path))


if __name__ == "__main__":
    main()
