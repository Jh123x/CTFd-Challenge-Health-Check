# Health Check for challenges

## Prerequisites

1. OS must support `nc` command to check servers with `nc`.
2. Python Virtual Environment

## Quick start

1. Clone this part of the repository
2. Create a python3 virtual environment using `python3 -m venv env`
3. Activate the environment `source env/bin/activate`
4. Install requirements `pip install -r requirements.txt`
5. Create a `.env` file with the format in [example files](#example-files)
6. Add an entry to crontab for the necessary interval

## How it works

1. Fetches challenge information from CTFd
2. Looks into `connection name` within CTFd challenges
3. If it starts with `http` or `https` it is added to the health check via `http`
4. If it starts with `nc` it is checked by using the `nc -nz` command

## Example files

### `.env` file

```ini
TELEGRAM_TOKEN=""       # Telegram bot token
TELEGRAM_CHAT_ID=""     # Telegram group chat id

CTFD_URL=""             # CTFd URL
CTFD_API_KEY=""         # API Key to access the challenges
```

### `Crontab -e` entry

This line will ensure that the script runs every 10 minutes and log the `stdout` to `/root/health_check/status.log`

```cron
*/10 * * * * { source /root/health_check/env/bin/activate && python3 /root/health_check/app.py && deactivate; } >> /root/health_check/status.log 2>&1
```

## Supported checks

- Status 200 on websites
- `nc` connectivity

## Future plans

1. Testing solution scripts to see if challenges work
2. More methods of checking if the server is up
