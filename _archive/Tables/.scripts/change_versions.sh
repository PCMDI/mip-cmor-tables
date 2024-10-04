for file in ./*.json; do
  # Backup the original file
  cp "$file" "$file.bak"

  # Apply changes to the JSON file using jq
  jq '.Header.Conventions |= sub("CMIP-6.3"; "CMIP-6.5") |
      .Header.cmor_version |= sub("3.7.3"; "3.8.0") |
      .Header.data_specs_version |= sub("6.3.0.0"; "6.5.0.0")' "$file" > "$file.tmp" && mv "$file.tmp" 
"$file" && rm "$file.bak"
done



