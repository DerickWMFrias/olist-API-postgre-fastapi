#!/usr/bin/env bash
set -e
exec 2> /docker-entrypoint-initdb.d/errorlogs/03_errors.txt
echo "PRODUCTS: Importando dados"


# Caminhos internos do container
CSV_PATH="/docker-entrypoint-initdb.d/olist_data/olist_products_dataset.csv"
DB_NAME="$POSTGRES_DB"
TABLE_NAME="PRODUCTS"

SQL_FILE=$(mktemp)
counter=0
round=0

# Lista de colunas explicitamente definidas (ordem deve corresponder ao CSV)
COLUMNS="product_id, product_category_name, product_name_lenght, product_description_lenght, product_photos_qty, product_weight_g, product_length_cm, product_height_cm, product_width_cm"
#echo "BEGIN;" > "$SQL_FILE"

# Lê cada linha do CSV (ignorando cabeçalho)
tail -n +2 "$CSV_PATH" | while IFS=',' read -r pid cat_name name_l desc_l photos_qty weight length height width; do
  # Escapa aspas simples
  pid=$(echo "$pid" | sed 's/^"//; s/"$//; s/"/'\''/g')
  pid=$(echo "$pid" | sed -E 's/^(.{8})(.{4})(.{4})(.{4})(.{12})$/\1-\2-\3-\4-\5/') #Formata UUID para conter hífens
  cat_name=$(echo "$cat_name" | sed 's/^"//; s/"$//; s/"/'\''/g')
  name_l=$(echo "$name_l" | sed 's/^"//; s/"$//; s/"/'\''/g')
  desc_l=$(echo "$desc_l" | sed 's/^"//; s/"$//; s/"/'\''/g')
  photos_qty=$(echo "$photos_qty" | sed 's/^"//; s/"$//; s/"/'\''/g')
  weight=$(echo "$weight" | sed 's/^"//; s/"$//; s/"/'\''/g')
  length=$(echo "$length" | sed 's/^"//; s/"$//; s/"/'\''/g')
  height=$(echo "$height" | sed 's/^"//; s/"$//; s/"/'\''/g')
  width=$(echo "$width" | sed 's/^"//; s/"$//; s/"/'\''/g') 
  

  # Cria SQL para uma linha
  #SQL="INSERT INTO $TABLE_NAME ($COLUMNS) VALUES ('$pid', '$cat_name', '$name_l', '$desc_l', '$photos_qty', '$weight', '$length', '$height', '$width');"

  # Cria SQL para uma linha
  printf "INSERT INTO %s (%s) VALUES ('%s', \$\$%s\$\$, '%s', '%s', '%s', '%s', '%s', '%s', '%s') ON CONFLICT (product_id) DO NOTHING;\n" \
    "$TABLE_NAME" "$COLUMNS" "$pid" "$cat_name" "$name_l" "$desc_l" "$photos_qty" "$weight" "$length" "$height" "$width" >> "$SQL_FILE"

  counter=$(expr $counter + 1)
  if [ $(expr $counter % 1000) -eq 0 ]; then
    current_time=$(date '+%H:%M:%S')
    round=$(expr $round + 1)
    printf "PRODUCTS: Dumpando 1000 entradas pro banco de dados no horário %s ; Round: %s\n" "$current_time" "$round"
      
    #echo "COMMIT;" >> "$SQL_FILE"
    psql -U "$POSTGRES_USER" -d "$DB_NAME" -f "$SQL_FILE" > /dev/null

    > "$SQL_FILE"
    #echo "BEGIN;" > "$SQL_FILE"
  fi
done

#echo "COMMIT;" >> "$SQL_FILE"
psql -U "$POSTGRES_USER" -d "$DB_NAME" -f "$SQL_FILE" > /dev/null

rm "$SQL_FILE"


echo "PRODUCTS: Importação concluída!"
echo ""
