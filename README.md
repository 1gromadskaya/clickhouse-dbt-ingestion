# Astronauts ELT Pipeline (API -> ClickHouse -> dbt)

A simple and reliable ELT (Extract, Load, Transform) pipeline that collects data about astronauts currently in space, saves it into a ClickHouse database, and transforms it into clean analytical tables using dbt.

## 🛠 Tech Stack
- **Python** (Requests, python-dotenv, clickhouse-connect)
- **ClickHouse** (Docker, ReplacingMergeTree, Materialized Views)
- **dbt (Data Build Tool)** (dbt-clickhouse)
- **Docker & Docker Compose**

## 🏗 Pipeline Architecture

1. **Extract & Load (Python):** 
   - A Python script (`ingest.py`) fetches raw data from the public Open-Notify API.
   - It includes a built-in retry mechanism (up to 5 attempts with delay) to handle network issues safely.

2. **Storage & Parsing (ClickHouse):** 
   - Raw JSON data is saved into the `raw_astros` table.
   - A **Materialized View** (`mv_raw_to_people`) automatically parses the JSON and populates the main `people` table.
   - Data deduplication is handled by the `ReplacingMergeTree` engine.

3. **Transform (dbt):**
   - **Staging (`stg_astros`):** Prepares and cleans the source data using text formatting (`trim`).
   - **Marts (`fct_craft_crew`):** Aggregates the data to count the number of crew members on each spacecraft.

## 📸 Project Results (Screenshots)

### 1. Target Table `people` (Parsed Data)
![People Table](images/People Table.png)
*Raw JSON successfully parsed and loaded into the relational table.*

### 2. Analytical Mart `fct_craft_crew` (dbt Model)
![Craft Crew Mart](images/Craft Crew Mart.png)
*Final aggregated view showing crew counts by spacecraft.*
