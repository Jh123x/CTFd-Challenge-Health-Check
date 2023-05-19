from requests import Session
from typing import List, Tuple
import logging


from .target import TARGET, create_generic_target


def generate_services(ctfd_url: str, ctfd_token: str) -> Tuple[List[TARGET], int]:
    """
    Generate a list of services to check out of total number of services
    [List of services, total number of services]
    """
    services = []
    with Session() as s:
        s.headers.update({"Authorization": f"Token {ctfd_token}"})
        url = f"{ctfd_url}/api/v1/challenges"
        resp = s.get(url, headers={
            "Content-Type": "application/json",
        })
        data = resp.json()
        results = data.get('data', [])

        for result in results:
            id = result.get('id')
            resp2 = s.get(f"{ctfd_url}/api/v1/challenges/{id}")
            challenge_date = resp2.json().get('data', {})
            connection_info = challenge_date.get('connection_info', None)
            name = challenge_date.get('name', None)

            if connection_info is None:
                logging.info(
                    f"Skipping challenge {id} because it has no connection info")
                continue

            target = create_generic_target(name, connection_info)
            if target is None:
                logging.info(
                    f"Skipping challenge {id} because it has no connection info")
                continue

            services.append(target)

    return services, len(results)
