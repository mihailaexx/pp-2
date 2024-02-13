import os
path = input()
if os.path.exists(path):
    print(f"existence: {os.access(path, os.F_OK)}")
    print(f"read: {os.access(path, os.R_OK)}")
    print(f"write: {os.access(path, os.W_OK)}")
    print(f"execute: {os.access(path, os.X_OK)}")
else:
    print("No such dir/file or directory")