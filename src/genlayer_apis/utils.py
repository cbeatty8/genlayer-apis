"""
Time and utility helpers for GenLayer Intelligent Contracts.

Provides timestamp conversion, date formatting, and common utilities.
All functions are pure Python — no external API calls needed.
"""

import json
from datetime import datetime, timezone


def timestamp_now() -> int:
    """
    Get current Unix timestamp in seconds.

    :returns: Current Unix timestamp

    Example::

        ts = timestamp_now()
        # 1711800000
    """
    return int(datetime.now(timezone.utc).timestamp())


def timestamp_to_iso(ts: int) -> str:
    """
    Convert Unix timestamp to ISO 8601 format.

    :param ts: Unix timestamp in seconds
    :returns: ISO 8601 formatted string

    Example::

        iso = timestamp_to_iso(1711800000)
        # '2024-03-30T12:00:00+00:00'
    """
    return datetime.fromtimestamp(ts, tz=timezone.utc).isoformat()


def iso_to_timestamp(iso: str) -> int:
    """
    Convert ISO 8601 string to Unix timestamp.

    :param iso: ISO 8601 formatted date string
    :returns: Unix timestamp in seconds

    Example::

        ts = iso_to_timestamp("2024-03-30T12:00:00Z")
        # 1711800000
    """
    # Handle Z suffix
    iso = iso.replace("Z", "+00:00")
    return int(datetime.fromisoformat(iso).timestamp())


def time_ago(ts: int) -> str:
    """
    Convert Unix timestamp to human-readable relative time.

    :param ts: Unix timestamp in seconds
    :returns: Human-readable string like "2 hours ago", "3 days ago"

    Example::

        ago = time_ago(1711800000)
        # '2 hours ago'
    """
    now = int(datetime.now(timezone.utc).timestamp())
    diff = now - ts

    if diff < 60:
        return f"{diff} seconds ago"
    elif diff < 3600:
        return f"{diff // 60} minutes ago"
    elif diff < 86400:
        return f"{diff // 3600} hours ago"
    elif diff < 2592000:
        return f"{diff // 86400} days ago"
    elif diff < 31536000:
        return f"{diff // 2592000} months ago"
    else:
        return f"{diff // 31536000} years ago"


def format_number(n: int | float, decimals: int = 2) -> str:
    """
    Format a number with commas and optional decimals.

    :param n: Number to format
    :param decimals: Number of decimal places (default 2)
    :returns: Formatted string

    Example::

        s = format_number(1234567.89)
        # '1,234,567.89'
    """
    if isinstance(n, int):
        return f"{n:,}"
    return f"{n:,.{decimals}f}"


def format_usd(n: float) -> str:
    """
    Format a number as USD currency.

    :param n: Amount to format
    :returns: Formatted string like "$1,234.56"

    Example::

        s = format_usd(1234.5)
        # '$1,234.50'
    """
    return f"${n:,.2f}"


def truncate_string(s: str, max_len: int = 100, suffix: str = "...") -> str:
    """
    Truncate a string to max_len, adding suffix if truncated.

    :param s: String to truncate
    :param max_len: Maximum length (default 100)
    :param suffix: Suffix to add when truncated (default "...")
    :returns: Truncated string

    Example::

        s = truncate_string("Very long text...", max_len=20)
        # 'Very long text...'
    """
    if len(s) <= max_len:
        return s
    return s[:max_len - len(suffix)] + suffix


def bytes_to_hex(data: bytes) -> str:
    """
    Convert bytes to hex string with 0x prefix.

    :param data: Bytes to convert
    :returns: Hex string like "0xdeadbeef"

    Example::

        h = bytes_to_hex(b"\\xde\\xad\\xbe\\xef")
        # '0xdeadbeef'
    """
    return "0x" + data.hex()


def hex_to_bytes(hex_str: str) -> bytes:
    """
    Convert hex string to bytes (with or without 0x prefix).

    :param hex_str: Hex string
    :returns: Decoded bytes

    Example::

        b = hex_to_bytes("0xdeadbeef")
        # b'\\xde\\xad\\xbe\\xef'
    """
    if hex_str.startswith("0x") or hex_str.startswith("0X"):
        hex_str = hex_str[2:]
    return bytes.fromhex(hex_str)
