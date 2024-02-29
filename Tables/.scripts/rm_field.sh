#!/bin/bash

directory_path="./"

for file_path in "$directory_path"/*.json; do
    if [ -f "$file_path" ]; then
        # Use jq to remove the entire "product" entry from the file
        if jq 'del(.Header.product)' "$file_path" > temp.json; then
            mv temp.json "$file_path"
            echo "Removed product entry from: $file_path"
        fi
    fi
done
