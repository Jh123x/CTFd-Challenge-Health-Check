import requests
import logging


def check_http(target_ip: str, port: int) -> bool:
    url = f"http://{target_ip}:{port}" if port != 80 else f"http://{target_ip}"
    with requests.Session() as s:
        resp = s.get(url)
        logging.info(f"Received status code {resp.status_code} for {url}")
        return resp.status_code == 200
