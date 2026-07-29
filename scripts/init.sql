CREATE TABLE IF NOT EXISTS default.raw_astros
(
    raw_json String,
    _inserted_at DateTime DEFAULT now()
)
ENGINE = MergeTree()
ORDER BY _inserted_at;

CREATE TABLE IF NOT EXISTS default.people
(
    craft String,
    name String,
    _inserted_at DateTime
)
ENGINE = ReplacingMergeTree(_inserted_at)
PRIMARY KEY (craft, name)
ORDER BY (craft, name);

CREATE MATERIALIZED VIEW IF NOT EXISTS default.mv_raw_to_parsed_astros
TO default.parsed_astros AS
SELECT
    tupleElement(person, 'craft') AS craft,
    tupleElement(person, 'name') AS name,
    _inserted_at
FROM default.raw_astros
ARRAY JOIN JSONExtract(raw_json, 'people', 'Array(Tuple(craft String, name String))') AS person;