import re
from typing import Tuple


PORT = int
IP = str

NC_PATTERN = re.compile(r"nc\s+(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s+(\d+)")
HTTP_PATTERN = re.compile(
    r"(http|https)://(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(:(\d+))?")


def parse_nc(connection_str: str) -> Tuple[IP, PORT]:
    """Parse the nc connection string"""
    match = NC_PATTERN.match(connection_str)
    if not match:
        raise ValueError(f"Invalid nc connection string: {connection_str}")

    ip, port = match.groups()
    return ip, int(port)


def parse_http(connection_str: str) -> Tuple[IP, PORT]:
    """Parse the http connection string"""
    match = HTTP_PATTERN.match(connection_str)
    if not match:
        raise ValueError(f"Invalid http connection string: {connection_str}")

    scheme, ip, _, port = match.groups()
    return ip, int(port) if port else 80
