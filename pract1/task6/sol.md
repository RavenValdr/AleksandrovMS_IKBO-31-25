#!/bin/bash

# Включаем поиск по подпапкам и защиту от пустых результатов
shopt -s nullglob globstar

for file in **/*.{c,js,py}; do
    firstLine="$(head -n 1 "$file")"


    if [[ "$file" == *.py ]]; then
        if grep -q '^#' <<< "$firstLine"; then
            echo "$file" # Выводим имя файла
        fi
    elif [[ "$file" == *.c || "$file" == *.js ]]; then
        if grep -qE '^(//|/\*)' <<< "$firstLine"; then
            echo "$file" # Выводим имя файла
        fi
    fi
done

