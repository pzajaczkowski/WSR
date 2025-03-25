#!/bin/bash

FILE_PARAM=$1
echo "File: $FILE_PARAM"

for file in "$FILE_PARAM."*; do
    mv "$file" "$2"
done