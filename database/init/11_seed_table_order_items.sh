#!/usr/bin/env bash
set -e
exec 2> /docker-entrypoint-initdb.d/errorlogs/10_errors.txt
echo "ORDER ITEMS: Importando dados"

# Caminhos internos do container
CSV_PATH="/docker-entrypoint-initdb.d/olist_data/olist_order_items_dataset.csv"
DB_NAME="$POSTGRES_DB"
STAGE_TABLE_NAME="STAGE_ORDER_ITEMS"
TABLE_NAME="ORDER_ITEMS"
COLUMNS="order_id, order_item_id , product_id, seller_id, shipping_limit_date, price, freight_value"




psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "CREATE TABLE $STAGE_TABLE_NAME (LIKE $TABLE_NAME);"

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\copy $STAGE_TABLE_NAME ($COLUMNS) 
FROM '$CSV_PATH' 
WITH (FORMAT csv, HEADER true, NULL '', ENCODING 'UTF-8')"

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "INSERT INTO $TABLE_NAME ($COLUMNS)
SELECT $COLUMNS
FROM $STAGE_TABLE_NAME st 
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.order_id = st.order_id)
AND EXISTS (SELECT 1 FROM products p WHERE p.product_id = st.product_id)
AND EXISTS (SELECT 1 FROM sellers s WHERE s.seller_id = st.seller_id)
ON CONFLICT (order_id, order_item_id, product_id, seller_id) DO NOTHING"

psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "DROP TABLE $STAGE_TABLE_NAME"

echo "ORDER ITEMS: Dados importados!"