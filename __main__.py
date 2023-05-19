import os
import logging
import argparse
from telebot import TeleBot
from dotenv import load_dotenv

from handlers import SERVICE_DICT
from common import generate_services
from config_generator import generate_default_env


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def check_service(target_ip: str, port: int, method: str) -> bool:
    """Returns true if the service is up"""
    method_func = SERVICE_DICT.get(method.lower(), None)
    if method_func is None:
        logging.critical(
            f"Unknown method: {method} for {target_ip}:{port}"
        )
        return False

    return method_func(target_ip, port)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--local",
        action="store_true",
        help="Run locally without sending message to telegram",
        default=False,
    )

    args = parser.parse_args()

    if generate_default_env():
        logging.info(
            "Generated default .env file. Please fill in the details.")
        exit(0)

    load_dotenv()

    ctfd_url = os.getenv("CTFD_URL", None)
    ctfd_token = os.getenv("CTFD_API_KEY", None)

    if None in [ctfd_url, ctfd_token]:
        logging.critical("CTFd URL or API key not set.")
        exit(1)

    if args.local:
        logging.info("Running locally without telegram")

    no_down = 0
    summary = []
    services, total_challs = generate_services(ctfd_url, ctfd_token)
    logging.info(f"Checking {len(services)} services...")

    for service in services:
        target_domain = service['target_domain']
        target_port = service['target_port']
        method = service['method']
        name = service['name']

        if check_service(target_domain, target_port, method):
            msg = f"{name} at {target_domain}:{target_port} is up. (method: {method})"
            logging.info(msg)
            continue

        no_down += 1
        msg = f"{name} @ {target_domain}:{target_port} is down. (method: {method})."
        summary.append(msg)
        logging.error(msg)

    if no_down == 0:
        msg = "✅ All services are up."
        summary.append(msg)
        logging.info(msg)
    else:
        msg = f"⚠{no_down} service(s) down!"
        summary.insert(0, msg)
        logging.error(msg)

    summary_info = f"`{len(services) - no_down}` up & `{no_down}` down of `{total_challs}` challenges."
    logging.info(summary_info)

    if not args.local:
        token = os.getenv("TELEGRAM_TOKEN", None)
        chat = os.getenv("TELEGRAM_CHAT_ID", None)

        if None in [token, chat]:
            logging.critical(
                "Unable to send message. Telegram token or chat id not set.")
            exit(1)
        bot = TeleBot(token=token)
        summary.append(summary_info)
        bot.send_message(chat, '\n'.join(summary), parse_mode="Markdown")

    logging.info("Health check completed.")
