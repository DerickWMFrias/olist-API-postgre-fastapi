#!/usr/bin/env bash
set -e
exec 2> /docker-entrypoint-initdb.d/errorlogs/09_errors.txt
echo "ORDER_REVIEWS: Importando dados"
#echo "$POSTGRES_DB"
#echo "$POSTGRES_USER"
#echo $POSTGRES_DB
#echo $POSTGRES_USER

# Caminhos internos do container
CSV_PATH="/docker-entrypoint-initdb.d/olist_data/olist_order_reviews_dataset.csv"
DB_NAME="$POSTGRES_DB"
STAGE_TABLE_NAME="STAGE_ORDER_REVIEWS"
TABLE_NAME="ORDER_REVIEWS"

#psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "CREATE TABLE $STAGE_TABLE_NAME (LIKE order_reviews INCLUDING ALL);"
#psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\d $STAGE_TABLE_NAME"
#psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "DROP TABLE $STAGE_TABLE_NAME"
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "CREATE TABLE $STAGE_TABLE_NAME (LIKE order_reviews);"
#psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\d $STAGE_TABLE_NAME"
#psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "ALTER TABLE $STAGE_TABLE_NAME DROP CONSTRAINT order_reviews_pk;"
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "\copy $STAGE_TABLE_NAME(review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp) FROM '$CSV_PATH' WITH (FORMAT csv, HEADER true, NULL '', FORCE_NOT_NULL (review_comment_title, review_comment_message), ENCODING 'UTF-8')" 
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "INSERT INTO $TABLE_NAME(review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp) 
SELECT review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp 
FROM $STAGE_TABLE_NAME s 
WHERE EXISTS (SELECT 1 FROM orders o WHERE o.order_id = s.order_id)
ON CONFLICT (review_id) DO NOTHING"
psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" -c "DROP TABLE $STAGE_TABLE_NAME"

echo "ORDER_REVIEWS: Dados importados!"