import os
from dotenv import load_dotenv

load_dotenv()

MAX_RETRIES = 5
INITIAL_BACKOFF = 2

API_URL = os.getenv("API_URL")

CH_HOST = os.getenv("CLICKHOUSE_HOST")
CH_PORT = int(os.getenv("CLICKHOUSE_HTTP_PORT"))
CH_USER = os.getenv("CLICKHOUSE_USER")
CH_PASSWORD = os.getenv("CLICKHOUSE_PASSWORD")
CH_DB = os.getenv("CLICKHOUSE_DB")