#!/usr/bin/env bash
set -e
exec 2> /docker-entrypoint-initdb.d/errorlogs/06_errors.txt
echo "ORDERS: Importando dados"


format_value() {
  local val="$1"
  local default="$2"
  
  if [ -z "$val" ]; then
    # Se $val está vazia (a condição é VERDADEIRA), usamos o valor padrão.
    echo "$default"
  else
    # Se $val NÃO está vazia (a condição é FALSA), usamos o valor de $val.
    echo "$val"
  fi
}

# Caminhos internos do container
CSV_PATH="/docker-entrypoint-initdb.d/olist_data/olist_orders_dataset.csv"
DB_NAME="$POSTGRES_DB"
TABLE_NAME="ORDERS"

SQL_FILE=$(mktemp)
counter=0
round=0

# Lista de colunas explicitamente definidas (ordem deve corresponder ao CSV)
COLUMNS="order_id, customer_id, order_status, order_purchase_timestamp, order_approved_at, order_delivered_carrier_date, order_delivered_customer_date, order_estimated_delivery_date"
#echo "BEGIN;" > "$SQL_FILE"

# Lê cada linha do CSV (ignorando cabeçalho)
tail -n +2 "$CSV_PATH" | while IFS=',' read -r oid cid status purchaset approvedat carrierdt customerdt deliverydt; do
  # Escapa aspas simples
  oid=$(echo "$oid" | sed 's/^"//; s/"$//; s/"/'\''/g')
  oid=$(echo "$oid" | sed -E 's/^(.{8})(.{4})(.{4})(.{4})(.{12})$/\1-\2-\3-\4-\5/') #Formata UUID para conter hífens
  cid=$(echo "$cid" | sed 's/^"//; s/"$//; s/"/'\''/g')
  cid=$(echo "$cid" | sed -E 's/^(.{8})(.{4})(.{4})(.{4})(.{12})$/\1-\2-\3-\4-\5/') #Formata UUID para conter hífens
  status=$(echo "$status" | sed 's/^"//; s/"$//; s/"/'\''/g')
  purchaset=$(echo "$purchaset" | sed 's/^"//; s/"$//; s/"/'\''/g')
  approvedat=$(echo "$approvedat" | sed 's/^"//; s/"$//; s/"/'\''/g')
  carrierdt=$(echo "$carrierdt" | sed 's/^"//; s/"$//; s/"/'\''/g')
  customerdt=$(echo "$customerdt" | sed 's/^"//; s/"$//; s/"/'\''/g')
  deliverydt=$(echo "$deliverydt" | sed 's/^"//; s/"$//; s/"/'\''/g')

  # Cria SQL para uma linha
  #SQL="INSERT INTO $TABLE_NAME ($COLUMNS) VALUES ('$oid', '$cid', '$status', '$purchaset', '$approvedat', '$carrierdt', '$customerdt', '$deliverydt');"

  # Cria SQL para uma linha
  printf "INSERT INTO %s (%s) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s') ON CONFLICT (order_id) DO NOTHING;\n" \
    "$TABLE_NAME" "$COLUMNS" "$oid" "$cid" "$status" "$purchaset" "$approvedat" "$carrierdt" "$customerdt" "$deliverydt" >> "$SQL_FILE"
  counter=$(expr $counter + 1)
  if [ $(expr $counter % 1000) -eq 0 ]; then
    current_time=$(date '+%H:%M:%S')
    round=$(expr $round + 1)
    printf "ORDERS: Dumpando 1000 entradas pro banco de dados no horário %s ; Round: %s\n" "$current_time" "$round"
      
    #echo "COMMIT;" >> "$SQL_FILE"
    psql -U "$POSTGRES_USER" -d "$DB_NAME" -f "$SQL_FILE" > /dev/null

    > "$SQL_FILE"
    #echo "BEGIN;" > "$SQL_FILE"
  fi
done

#echo "COMMIT;" >> "$SQL_FILE"
psql -U "$POSTGRES_USER" -d "$DB_NAME" -f "$SQL_FILE" > /dev/null

rm "$SQL_FILE"


echo "ORDERS: Importação concluída!"
echo ""
