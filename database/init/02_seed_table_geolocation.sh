#!/usr/bin/env bash
set -e
exec 2> /docker-entrypoint-initdb.d/errorlogs/02_errors.txt

echo "GEOLOCATION: Importando dados"


# Caminhos internos do container
CSV_PATH="/docker-entrypoint-initdb.d/olist_data/olist_geolocation_dataset.csv"
DB_NAME="$POSTGRES_DB"
TABLE_NAME="GEOLOCATION"

SQL_FILE=$(mktemp)
counter=0
round=0
# Lista de colunas explicitamente definidas (ordem deve corresponder ao CSV)
COLUMNS="geolocation_zip_code_prefix, geolocation_lat, geolocation_lng, geolocation_city, geolocation_state"
#echo "BEGIN;" > "$SQL_FILE"

# Lê cada linha do CSV (ignorando cabeçalho)
tail -n +2 "$CSV_PATH" | while IFS=',' read -r zipcode lat lng city state; do
  # Escapa aspas simples
  zipcode=$(echo "$zipcode" | sed 's/^"//; s/"$//; s/"/'\''/g')
  lat=$(echo "$lat" | sed 's/^"//; s/"$//; s/"/'\''/g')
  lng=$(echo "$lng" | sed 's/^"//; s/"$//; s/"/'\''/g')
  city=$(echo "$city" | sed 's/^"//; s/"$//; s/"/'\''/g')
  state=$(echo "$state" | sed 's/^"//; s/"$//; s/"/'\''/g')

  # Cria SQL para uma linha
  printf "INSERT INTO %s (%s) VALUES ('%s', '%s', '%s', \$\$%s\$\$, '%s') ON CONFLICT (geolocation_zip_code_prefix) DO NOTHING;\n" \
    "$TABLE_NAME" "$COLUMNS" "$zipcode" "$lat" "$lng" "$city" "$state" >> "$SQL_FILE"

  counter=$(expr $counter + 1)
  if [ $(expr $counter % 1000) -eq 0 ]; then
    current_time=$(date '+%H:%M:%S')
    round=$(expr $round + 1)
    printf "GEOLOCATION: Dumpando 1000 entradas pro banco de dados no horário %s ; Round: %s\n" "$current_time" "$round"
      
    #echo "COMMIT;" >> "$SQL_FILE"
    psql -U "$POSTGRES_USER" -d "$DB_NAME" -f "$SQL_FILE" > /dev/null

    > "$SQL_FILE"
    #echo "BEGIN;" > "$SQL_FILE"
  fi
done

#echo "COMMIT;" >> "$SQL_FILE"
psql -U "$POSTGRES_USER" -d "$DB_NAME" -f "$SQL_FILE" > /dev/null

rm "$SQL_FILE"

echo "GEOLOCATION: Importação concluída!"
echo ""
