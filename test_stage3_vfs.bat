@echo off
echo === Test 1: Minimal VFS ===
python -m src.emulator --vfs vfs_samples/minimal --script scripts/stage3_test.txt

echo === Test 2: Multi-file VFS ===
python -m src.emulator --vfs vfs_samples/multi_files --script scripts/stage3_test.txt

echo === Test 3: 3-level deep VFS ===
python -m src.emulator --vfs vfs_samples/deep_tree --script scripts/stage3_test.txt

echo === Test 4: Error - VFS directory not found ===
python -m src.emulator --vfs vfs_samples/non_existent_vfs

echo === Test 5: Error - VFS path is a file, not a directory ===
python -m src.emulator --vfs README.md
