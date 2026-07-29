import time
import logging
import requests
import clickhouse_connect
import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def fetch_astros_raw_json(url: str) -> str:
    attempt = 1
    backoff = config.INITIAL_BACKOFF

    while attempt <= config.MAX_RETRIES:
        try:
            logging.info(f"Attempt {attempt}/{config.MAX_RETRIES}: Fetching {url}")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            logging.info("Successfully fetched JSON from Open-Notify API.")
            return response.text
        except requests.exceptions.RequestException as err:
            logging.warning(f"Request failed: {err}")
            if attempt == config.MAX_RETRIES:
                logging.error(f"Max retries reached ({config.MAX_RETRIES}). Aborting.")
                raise RuntimeError(f"Failed to fetch data after {config.MAX_RETRIES} attempts: {err}")
            time.sleep(backoff)
            backoff *= 2
            attempt += 1


def load_raw_json_to_clickhouse(raw_json_str: str) -> None:
    logging.info(f"Connecting to ClickHouse")
    client = clickhouse_connect.get_client(
        host=config.CH_HOST,
        port=config.CH_PORT,
        username=config.CH_USER,
        password=config.CH_PASSWORD,
        database=config.CH_DB
    )

    logging.info("Inserting raw JSON into 'raw_astros' table")
    client.insert(
        table='raw_astros',
        data=[[raw_json_str]],
        column_names=['raw_json']
    )

    logging.info("Optimizing 'people' table")
    client.command(f"OPTIMIZE TABLE {config.CH_DB}.people FINAL")

    logging.info("Data successfully loaded and materialized in ClickHouse")

def main():
    raw_json = fetch_astros_raw_json(config.API_URL)
    load_raw_json_to_clickhouse(raw_json)
    logging.info("Ingestion process completed successfully.")


if __name__ == "__main__":
    main()