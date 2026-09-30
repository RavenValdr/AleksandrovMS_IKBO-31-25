
#!/bin/bash


find . -type f -name "*.$1" -print0 | tar -cvf "archive_$1.tar" --null -T -
