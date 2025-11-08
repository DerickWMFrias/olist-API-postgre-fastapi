#!/usr/bin/env bash
set -e
exec 2> /docker-entrypoint-initdb.d/errorlogs/09_errors.txt
echo "ORDER_ITENS: Importando dados CSV para o banco..."

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
CSV_PATH="/docker-entrypoint-initdb.d/olist_data/olist_order_items_dataset.csv"
DB_NAME="$POSTGRES_DB"
TABLE_NAME="ORDER_ITENS"

SQL_FILE=$(mktemp)
counter=0
round=0

# Lista de colunas explicitamente definidas (ordem deve corresponder ao CSV)
COLUMNS="order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value"
#echo "BEGIN;" > "$SQL_FILE"

# Lê cada linha do CSV (ignorando cabeçalho)
tail -n +2 "$CSV_PATH" | while IFS=',' read -r oid oitid pid sid limitdt price freight; do
  # Escapa aspas simples
  oid=$(echo "$oid" | sed 's/^"//; s/"$//; s/"/'\''/g')
  oid=$(echo "$oid" | sed -E 's/^(.{8})(.{4})(.{4})(.{4})(.{12})$/\1-\2-\3-\4-\5/') #Formata UUID para conter hífens
  oitid=$(echo "$oitid" | sed 's/^"//; s/"$//; s/"/'\''/g')
  oitid=$(echo "$oitid" | sed -E 's/^(.{8})(.{4})(.{4})(.{4})(.{12})$/\1-\2-\3-\4-\5/') #Formata UUID para conter hífens
  pid=$(echo "$pid" | sed 's/^"//; s/"$//; s/"/'\''/g')
  pid=$(echo "$pid" | sed -E 's/^(.{8})(.{4})(.{4})(.{4})(.{12})$/\1-\2-\3-\4-\5/') #Formata UUID para conter hífens
  sid=$(echo "$sid" | sed 's/^"//; s/"$//; s/"/'\''/g')
  sid=$(echo "$sid" | sed -E 's/^(.{8})(.{4})(.{4})(.{4})(.{12})$/\1-\2-\3-\4-\5/') #Formata UUID para conter hífens
  limitdt=$(echo "$limitdt" | sed 's/^"//; s/"$//; s/"/'\''/g')
  price=$(echo "$price" | sed 's/^"//; s/"$//; s/"/'\''/g')
  freight=$(echo "$freight" | sed 's/^"//; s/"$//; s/"/'\''/g')

  # Cria SQL para uma linha
  #SQL="INSERT INTO $TABLE_NAME ($COLUMNS) VALUES ('$oid', '$oitid', '$pid', '$sid', '$limitdt', '$price', '$freight');"

  # Cria SQL para uma linha
  printf "INSERT INTO %s (%s) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s') ON CONFLICT (order_id, order_item_id, product_id, seller_id) DO NOTHING;\n" \
    "$TABLE_NAME" "$COLUMNS" "$oid" "$oitid" "$pid" "$sid" "$limitdt" "$price" "$freight" >> "$SQL_FILE"

  counter=$(expr $counter + 1)
  if [ $(expr $counter % 1000) -eq 0 ]; then
    current_time=$(date '+%H:%M:%S')
    round=$(expr $round + 1)
    printf "ORDER_ITENS: Dumpando 1000 entradas pro banco de dados no horário %s ; Round: %s\n" "$current_time" "$round"
      
    #echo "COMMIT;" >> "$SQL_FILE"
    psql -U "$POSTGRES_USER" -d "$DB_NAME" -f "$SQL_FILE" > /dev/null

    > "$SQL_FILE"
    #echo "BEGIN;" > "$SQL_FILE"
  fi
done

#echo "COMMIT;" >> "$SQL_FILE"
psql -U "$POSTGRES_USER" -d "$DB_NAME" -f "$SQL_FILE" > /dev/null

rm "$SQL_FILE"


echo "ORDER_ITENS: Importação concluída!"
echo ""
