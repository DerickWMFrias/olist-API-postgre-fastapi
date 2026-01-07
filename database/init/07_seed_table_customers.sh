#!/usr/bin/env bash
set -e
exec 2> /docker-entrypoint-initdb.d/errorlogs/05_errors.txt
echo "CUSTOMERS: Importando dados"

# Caminhos internos do container
CSV_PATH="/docker-entrypoint-initdb.d/olist_data/olist_customers_dataset.csv"
DB_NAME="$POSTGRES_DB"
STAGE_TABLE_NAME="STAGE_CUSTOMERS"
TABLE_NAME="CUSTOMERS"
COLUMNS="customer_id, customer_unique_id, customer_zip_code_prefix, customer_city, customer_state"


psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "CREATE TABLE $STAGE_TABLE_NAME (LIKE $TABLE_NAME);"

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\copy $STAGE_TABLE_NAME ($COLUMNS) 
FROM '$CSV_PATH' 
WITH (FORMAT csv, HEADER true, NULL '', ENCODING 'UTF-8')"

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "INSERT INTO $TABLE_NAME ($COLUMNS)
SELECT $COLUMNS
FROM $STAGE_TABLE_NAME c 
WHERE EXISTS (SELECT 1 FROM geolocation g WHERE g.geolocation_zip_code_prefix = c.customer_zip_code_prefix)
ON CONFLICT (customer_id) DO NOTHING"

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "DROP TABLE $STAGE_TABLE_NAME"



echo "CUSTOMERS: Dados importados!"