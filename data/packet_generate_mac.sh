#!/opt/homebrew/bin/bash

mkdir -p packets

# Sizes in bytes
declare -A sizes=(
  ["5mb"]=5242880
  # ["15mb"]=15728640
  # ["25mb"]=26214400
  # ["35mb"]=36700160
  # ["45mb"]=47185920
)

# Generate 5 files per size
for name in "${!sizes[@]}"; do
  size_bytes="${sizes[$name]}"
  dir="packets/${name}"
  mkdir -p "$dir"
  
  echo "Generating 5 files of size $name (~$((size_bytes / 1048576)) MB) ..."
  
  for i in $(seq -w 1 5); do
    head -c "$size_bytes" /dev/urandom > "${dir}/${name}_${i}.bin"
  done
  
  echo "Created 5 files in ${dir}/"
done

echo "Packets generated."