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
