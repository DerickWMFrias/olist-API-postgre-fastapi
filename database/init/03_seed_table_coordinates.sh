#!/usr/bin/env bash
set -e
exec 2> /docker-entrypoint-initdb.d/errorlogs/03_errors.txt
echo "COORDINATES: Importando dados"

# Caminhos internos do container
CSV_PATH="/docker-entrypoint-initdb.d/olist_data/olist_geolocation_dataset.csv"
DB_NAME="$POSTGRES_DB"
STAGE_TABLE_NAME="STAGE_COORDINATES"
TABLE_NAME="COORDINATES"
COLUMNS_STAGE="geolocation_zip_code_prefix, lat, lng, geolocation_city, geolocation_state"
COLUMNS="geolocation_zip_code_prefix, lat, lng"

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "CREATE TABLE $STAGE_TABLE_NAME (
    geolocation_zip_code_prefix VARCHAR(8),
    lat NUMERIC(17,14),
    lng NUMERIC(17,14),
    geolocation_city VARCHAR(100),
    geolocation_state VARCHAR(16)
);"

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\copy $STAGE_TABLE_NAME ($COLUMNS_STAGE) 
FROM '$CSV_PATH' 
WITH (FORMAT csv, HEADER true, NULL '', ENCODING 'UTF-8')"

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "INSERT INTO $TABLE_NAME ($COLUMNS)
SELECT DISTINCT $COLUMNS
FROM $STAGE_TABLE_NAME s 
WHERE EXISTS (SELECT 1 FROM geolocation o WHERE o.geolocation_zip_code_prefix = s.geolocation_zip_code_prefix)
ON CONFLICT (lat, lng) DO NOTHING"

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "DROP TABLE $STAGE_TABLE_NAME"

echo "COORDINATES: Dados importados!"