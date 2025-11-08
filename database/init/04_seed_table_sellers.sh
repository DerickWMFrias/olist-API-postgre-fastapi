#!/usr/bin/env bash
set -e
exec 2> /docker-entrypoint-initdb.d/errorlogs/04_errors.txt
echo "SELLERS: Importando dados."

# Caminhos internos do container
CSV_PATH="/docker-entrypoint-initdb.d/olist_data/olist_sellers_dataset.csv"
DB_NAME="$POSTGRES_DB"
TABLE_NAME="SELLERS"

SQL_FILE=$(mktemp)
counter=0
round=0

# Lista de colunas explicitamente definidas (ordem deve corresponder ao CSV)
COLUMNS="seller_id, seller_zip_code_prefix, seller_city, seller_state"

#echo "BEGIN;" > "$SQL_FILE"

# Lê cada linha do CSV (ignorando cabeçalho)
tail -n +2 "$CSV_PATH" | while IFS=',' read -r iid zipcode city state; do
  # Escapa aspas simples
  iid=$(echo "$iid" | sed 's/^"//; s/"$//; s/"/'\''/g')
  iid=$(echo "$iid" | sed -E 's/^(.{8})(.{4})(.{4})(.{4})(.{12})$/\1-\2-\3-\4-\5/') #Formata UUID para conter hífens
  zipcode=$(echo "$zipcode" | sed 's/^"//; s/"$//; s/"/'\''/g')
  city=$(echo "$city" | sed 's/^"//; s/"$//; s/"/'\''/g')
  state=$(echo "$state" | sed 's/^"//; s/"$//; s/"/'\''/g')

  # Cria SQL para uma linha
  #SQL="INSERT INTO $TABLE_NAME ($COLUMNS) VALUES ('$iid', '$zipcode', '$city', '$state');"

  # Cria SQL para uma linha
  printf "INSERT INTO %s (%s) VALUES ('%s', '%s', \$\$%s\$\$, '%s') ON CONFLICT (seller_id) DO NOTHING;\n" \
    "$TABLE_NAME" "$COLUMNS" "$iid" "$zipcode" "$city" "$state" >> "$SQL_FILE"
  
  counter=$(expr $counter + 1)
  if [ $(expr $counter % 1000) -eq 0 ]; then
    current_time=$(date '+%H:%M:%S')
    round=$(expr $round + 1)
    printf "SELLERS: Dumpando 1000 entradas pro banco de dados no horário %s ; Round: %s\n" "$current_time" "$round"
      
    #echo "COMMIT;" >> "$SQL_FILE"
    psql -U "$POSTGRES_USER" -d "$DB_NAME" -f "$SQL_FILE" > /dev/null

    > "$SQL_FILE"
    #echo "BEGIN;" > "$SQL_FILE"
  fi
done

#echo "COMMIT;" >> "$SQL_FILE"
psql -U "$POSTGRES_USER" -d "$DB_NAME" -f "$SQL_FILE" > /dev/null

rm "$SQL_FILE"


echo "SELLERS: Importação concluída!"
echo ""