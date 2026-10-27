#!/usr/bin/env bash
set -e

mkdir -p /tmp/sample_vfs/docs
echo "Hello from root VFS" > /tmp/sample_vfs/hello.txt
echo "Documentation content" > /tmp/sample_vfs/docs/readme.txt

python3 -m src.emulator --vfs /tmp/sample_vfs "$@"
