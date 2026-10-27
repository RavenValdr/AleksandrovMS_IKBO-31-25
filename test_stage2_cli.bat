@echo off
echo === Test 1: Run with VFS and valid startup script ===
python -m src.emulator --vfs vfs_samples/minimal --script scripts/stage3_test.txt

echo === Test 2: Run with non-existent startup script ===
python -m src.emulator --vfs vfs_samples/minimal --script scripts/missing.txt
