#!/usr/bin/env bash
set -e
exec 2> /docker-entrypoint-initdb.d/errorlogs/07_errors.txt
echo "ORDER PAYMENTS: Importando dados"

# Caminhos internos do container
CSV_PATH="/docker-entrypoint-initdb.d/olist_data/olist_order_payments_dataset.csv"
DB_NAME="$POSTGRES_DB"
STAGE_TABLE_NAME="STAGE_ORDER_PAYMENTS"
TABLE_NAME="ORDER_PAYMENTS"
COLUMNS="order_id, payment_sequential, payment_type, payment_installments, payment_value"




psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "CREATE TABLE $STAGE_TABLE_NAME (LIKE $TABLE_NAME);"

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\copy $STAGE_TABLE_NAME ($COLUMNS) 
FROM '$CSV_PATH' 
WITH (FORMAT csv, HEADER true, NULL '', ENCODING 'UTF-8')"

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "INSERT INTO $TABLE_NAME ($COLUMNS)
SELECT $COLUMNS
FROM $STAGE_TABLE_NAME s 
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.order_id = s.order_id)
ON CONFLICT (order_id, payment_sequential) DO NOTHING"

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "DROP TABLE $STAGE_TABLE_NAME"

echo "ORDER PAYMENTS: Dados importados!"