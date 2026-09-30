Task 1
```
sort passwd | grep -o '^[^:]*'
```

Task 2
```
cd /etc

grep -v '^#' /etc/protocols | awk '{print $2, $1}' | sort -nr | head -n 5
```

Task 3
```
#!/bin/bash
text="$*"

len=${#text}

border=""
for (( i=0; i<len+2; i++ )); do
    border="$border-"
done

echo "+${border}+"
echo "| ${text} |"
echo "+${border}+"
```

Task 4
```
#!/bin/bash

if [ -z "$1" ]; then
    echo "Использование: ./get_ids <имя_файла>"
    exit 1
fi

grep -oE '[a-zA-Z_][a-zA-Z0-9_]*' "$1" | sort | uniq | xargs
```

Task 5
```
#!/bin/bash

chmod +x "$1"
sudo cp "$1" /usr/local/bin/
```

Task 6
```
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

```

Task 7
```
#!/bin/bash

# 1. Проверяем, передали ли нам путь к папке
if [ -z "$1" ]; then
    echo "Использование: $0 <путь_к_папке>"
    exit 1
fi

# 2. Проверяем, существует ли указанная папка
if [ ! -d "$1" ]; then
    echo "Ошибка: '$1' не является папкой или не существует."
    exit 1
fi

echo "Поиск дубликатов в папке '$1'..."
echo "------------------------------------------------"

find "$1" -type f -size +0 -exec md5sum {} + | sort | uniq -w 32 --all-repeated=separate
```

Task 8
```
#!/bin/bash


find . -type f -name "*.$1" -print0 | tar -cvf "archive_$1.tar" --null -T -
```

Task 9
```
#!/bin/bash

sed 's/    /\t/g' < "$1" > "$2"
```

Task 10
```
#!/bin/bash

# Проверяем, передали ли нам директорию
if [ -z "$1" ]; then
    echo "Использование: $0 <путь_к_директории>"
    exit 1
fi

# Проверяем, существует ли такая директория
if [ ! -d "$1" ]; then
    echo "Ошибка: директория '$1' не найдена."
    exit 1
fi

# Ищем пустые текстовые файлы
find "$1" -type f -empty -name "*.txt"
```
