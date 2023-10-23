# Remove the .html extension from files
for file in *.html; do
  mv "$file" "${file%.html}"
done

# Extract each zip into its own directory
for zip in *.zip; do
  dir_name=$(basename "$zip" .zip)
  mkdir "$dir_name"
  unzip "$zip" -d "$dir_name"
done
