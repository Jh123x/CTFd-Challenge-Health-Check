import subprocess
import logging


def check_nc(target_ip: str, port: int) -> bool:
    """Check if the server is up through nc"""
    try:
        # If the error code is 0, then the server is up, otherwise the server is down
        result = subprocess.run(
            ["nc", "-nz", target_ip, str(port)], check=True, timeout=1)
        logging.info(f"nc returned {result.returncode} for {target_ip}:{port}")
        return result.returncode == 0
    except Exception:
        logging.error(f"nc failed for {target_ip}:{port}")
        return False
