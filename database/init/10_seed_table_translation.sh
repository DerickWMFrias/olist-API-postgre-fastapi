#!/usr/bin/env bash
set -e
exec 2> /docker-entrypoint-initdb.d/errorlogs/10_errors.txt
echo "PRODUCT_CATEGORY_NAME_TRANSLATION: Importando dados"

# Caminhos internos do container
CSV_PATH="/docker-entrypoint-initdb.d/olist_data/product_category_name_translation.csv"
DB_NAME="$POSTGRES_DB"
TABLE_NAME="PRODUCT_CATEGORY_NAME_TRANSLATION" 

SQL_FILE=$(mktemp)
counter=0
round=0

# Lista de colunas explicitamente definidas (ordem deve corresponder ao CSV)
COLUMNS="product_category_name, product_category_name_english"
#echo "BEGIN;" > "$SQL_FILE"

# Lê cada linha do CSV (ignorando cabeçalho)
tail -n +2 "$CSV_PATH" | while IFS=',' read -r nome name; do
  # Escapa aspas simples
  nome=$(echo "$nome" | sed 's/^"//; s/"$//; s/"/'\''/g')
  name=$(echo "$name" | sed 's/^"//; s/"$//; s/"/'\''/g')
  #"s/'/''/g"
  # Cria SQL para uma linha
  #SQL="INSERT INTO $TABLE_NAME ($COLUMNS) VALUES ('$nome', '$name');"

  # Cria SQL para uma linha
  printf "INSERT INTO %s (%s) VALUES (\$\$%s\$\$, \$\$%s\$\$) ON CONFLICT (product_category_name, product_category_name_english) DO NOTHING;\n" \
    "$TABLE_NAME" "$COLUMNS" "$nome" "$name" >> "$SQL_FILE"

  counter=$(expr $counter + 1)
  if [ $(expr $counter % 1000) -eq 0 ]; then
    current_time=$(date '+%H:%M:%S')
    round=$(expr $round + 1)
    printf "PRODUCT_CATEGORY_NAME_TRANSLATION: Dumpando 1000 entradas pro banco de dados no horário %s ; Round: %s\n" "$current_time" "$round"
      
    #echo "COMMIT;" >> "$SQL_FILE"
    psql -U "$POSTGRES_USER" -d "$DB_NAME" -f "$SQL_FILE" > /dev/null

    > "$SQL_FILE"
    #echo "BEGIN;" > "$SQL_FILE"
  fi
done

#echo "COMMIT;" >> "$SQL_FILE"
psql -U "$POSTGRES_USER" -d "$DB_NAME" -f "$SQL_FILE" > /dev/null

rm "$SQL_FILE"


echo "PRODUCT_CATEGORY_NAME_TRANSLATION: Importação concluída!"
echo ""