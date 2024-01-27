"""Python library to use smsbox.net API."""

try:
    from ._version import version as __version__  # type: ignore
    from ._version import version_tuple  # type: ignore
except ImportError:
    __version__ = "unknown version"
    version_tuple = (0, 0, "unknown version")
