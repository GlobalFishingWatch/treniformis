"""Treniformis exceptions"""


class TreniformisException(Exception):
    """Base exception."""


class TreniformisIOError(IOError):
    """Asset does not exist or cannot be opened."""
