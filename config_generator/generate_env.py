import os
from .constants import DEFAULT_ENV_FILE


def generate_default_env() -> None:
    """Generates a default .env file if it does not exist."""
    if os.path.exists(".env"):
        return False

    with open(".env", "w") as f:
        f.write(DEFAULT_ENV_FILE)

    return True
