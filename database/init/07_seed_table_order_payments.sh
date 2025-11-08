#!/usr/bin/env bash
set -e
exec 2> /docker-entrypoint-initdb.d/errorlogs/07_errors.txt
echo "ORDER_PAYMENTS: Importando dados"


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
CSV_PATH="/docker-entrypoint-initdb.d/olist_data/olist_order_payments_dataset.csv"
DB_NAME="$POSTGRES_DB"
TABLE_NAME="ORDER_PAYMENTS"

SQL_FILE=$(mktemp)
counter=0
round=0

# Lista de colunas explicitamente definidas (ordem deve corresponder ao CSV)
COLUMNS="order_id, payment_sequential, payment_type, payment_installments, payment_value"
#echo "BEGIN;" > "$SQL_FILE"

# Lê cada linha do CSV (ignorando cabeçalho)
tail -n +2 "$CSV_PATH" | while IFS=',' read -r oid sequential type installments value; do
  # Escapa aspas simples
  oid=$(echo "$oid" | sed 's/^"//; s/"$//; s/"/'\''/g')
  oid=$(echo "$oid" | sed -E 's/^(.{8})(.{4})(.{4})(.{4})(.{12})$/\1-\2-\3-\4-\5/') #Formata UUID para conter hífens
  sequential=$(echo "$sequential" | sed 's/^"//; s/"$//; s/"/'\''/g')
  type=$(echo "$type" | sed 's/^"//; s/"$//; s/"/'\''/g')
  installments=$(echo "$installments" | sed 's/^"//; s/"$//; s/"/'\''/g')
  value=$(echo "$value" | sed 's/^"//; s/"$//; s/"/'\''/g')

  # Cria SQL para uma linha
  #SQL="INSERT INTO $TABLE_NAME ($COLUMNS) VALUES ('$oid', '$sequential', '$type', '$installments', '$value');"

  # Cria SQL para uma linha
  printf "INSERT INTO %s (%s) VALUES ('%s', '%s', '%s', '%s', '%s') ON CONFLICT (order_id, payment_sequential) DO NOTHING;\n" \
    "$TABLE_NAME" "$COLUMNS" "$oid" "$sequential" "$type" "$installments" "$value" >> "$SQL_FILE"

  counter=$(expr $counter + 1)
  if [ $(expr $counter % 1000) -eq 0 ]; then
    current_time=$(date '+%H:%M:%S')
    round=$(expr $round + 1)
    printf "ORDER_PAYMENTS: Dumpando 1000 entradas pro banco de dados no horário %s ; Round: %s\n" "$current_time" "$round"
      
    #echo "COMMIT;" >> "$SQL_FILE"
    psql -U "$POSTGRES_USER" -d "$DB_NAME" -f "$SQL_FILE" > /dev/null

    > "$SQL_FILE"
    #echo "BEGIN;" > "$SQL_FILE"
  fi
done

#echo "COMMIT;" >> "$SQL_FILE"
psql -U "$POSTGRES_USER" -d "$DB_NAME" -f "$SQL_FILE" > /dev/null

rm "$SQL_FILE"

echo "ORDER_PAYMENTS: Importação concluída!"
echo ""
