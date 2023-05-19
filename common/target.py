from typing import Dict, Optional
from .parsing import parse_http, parse_nc


TARGET = Dict[str, str]


def create_target(target_domain: str, port: int = 80, method: str = 'http', name: str = "") -> TARGET:
    """Create a target dictionary to be used in the health check."""
    return {
        "target_domain": target_domain,
        "target_port": port,
        "method": method,
        "name": name,
    }


def is_http_service(connection_str: str) -> bool:
    """Check if the connection string is an http service"""
    return connection_str.startswith("http") or connection_str.startswith("https")


def is_nc_service(connection_str: str) -> bool:
    """Check if the connection string is an nc service"""
    return connection_str.startswith("nc")


def create_generic_target(challenge_name: str, connection_str: str) -> Optional[TARGET]:
    """Create a target based on the connection string"""
    if is_http_service(connection_str):
        ip, port = parse_http(connection_str)
        return create_target(target_domain=ip, method="http", port=port, name=challenge_name)

    if is_nc_service(connection_str):
        # Use regex to get ip and port
        ip, port = parse_nc(connection_str)
        return create_target(target_domain=ip, method="nc", port=port, name=challenge_name)

    return None
