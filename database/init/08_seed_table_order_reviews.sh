#!/usr/bin/env bash
set -e
exec 2> /docker-entrypoint-initdb.d/errorlogs/08_errors.txt
echo "ORDER_REVIEWS: Importando dados"

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
CSV_PATH="/docker-entrypoint-initdb.d/olist_data/olist_order_reviews_dataset.csv"
DB_NAME="$POSTGRES_DB"
TABLE_NAME="ORDER_REVIEWS"

SQL_FILE=$(mktemp)
counter=0
round=0

# Lista de colunas explicitamente definidas (ordem deve corresponder ao CSV)
COLUMNS="review_id, order_id, review_score, review_comment_title, review_comment_message, review_creation_date, review_answer_timestamp"
#echo "BEGIN;" > "$SQL_FILE"

# Lê cada linha do CSV (ignorando cabeçalho)
tail -n +2 "$CSV_PATH" | while IFS=',' read -r rid oid rscore rtitle rmessage rcreationdt ranswertmst; do
  # Escapa aspas simples
  rid=$(echo "$rid" | sed 's/^"//; s/"$//; s/"/'\''/g')
  rid=$(echo "$rid" | sed -E 's/^(.{8})(.{4})(.{4})(.{4})(.{12})$/\1-\2-\3-\4-\5/') #Formata UUID para conter hífens
  oid=$(echo "$oid" | sed 's/^"//; s/"$//; s/"/'\''/g')
  oid=$(echo "$oid" | sed -E 's/^(.{8})(.{4})(.{4})(.{4})(.{12})$/\1-\2-\3-\4-\5/') #Formata UUID para conter hífens
  rscore=$(echo "$rscore" | sed 's/^"//; s/"$//; s/"/'\''/g')
  rtitle=$(echo "$rtitle" | sed 's/^"//; s/"$//; s/"/'\''/g')
  rmessage=$(echo "$rmessage" | sed 's/^"//; s/"$//; s/"/'\''/g')
  rcreationdt=$(echo "$rcreationdt" | sed 's/^"//; s/"$//; s/"/'\''/g')
  ranswertmst=$(echo "$ranswertmst" | sed 's/^"//; s/"$//; s/"/'\''/g')

  # Cria SQL para uma linha
  #SQL="INSERT INTO $TABLE_NAME ($COLUMNS) VALUES ('$rid', '$oid', '$rscore', '$rtitle', '$rmessage', '$rcreationdt', '$ranswertmst');"

  # Cria SQL para uma linha
  printf "INSERT INTO %s (%s) VALUES ('%s', '%s', '%s', \$\$%s\$\$, \$\$%s\$\$, '%s', '%s') ON CONFLICT (review_id) DO NOTHING;\n" \
    "$TABLE_NAME" "$COLUMNS" "$rid" "$oid" "$rscore" "$rtitle" "$rmessage" "$rcreationdt" "$ranswertmst" >> "$SQL_FILE"

  counter=$(expr $counter + 1)
  if [ $(expr $counter % 1000) -eq 0 ]; then
    current_time=$(date '+%H:%M:%S')
    round=$(expr $round + 1)
    printf "ORDER_REVIEWS: Dumpando 1000 entradas pro banco de dados no horário %s ; Round: %s\n" "$current_time" "$round"
      
    #echo "COMMIT;" >> "$SQL_FILE"
    psql -U "$POSTGRES_USER" -d "$DB_NAME" -f "$SQL_FILE" > /dev/null

    > "$SQL_FILE"
    #echo "BEGIN;" > "$SQL_FILE"
  fi
done

#echo "COMMIT;" >> "$SQL_FILE"
psql -U "$POSTGRES_USER" -d "$DB_NAME" -f "$SQL_FILE" > /dev/null

rm "$SQL_FILE"


echo "ORDER_REVIEWS: Importação concluída!"
echo ""
