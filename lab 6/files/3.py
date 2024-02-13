import os
path = input()
if os.path.exists(path):
    print("Correct path!")
    print(f"Directory: {os.path.dirname(path)}")
    if os.path.isdir(path):
        print("Dir include files:")
        print(*os.listdir(path), sep="\n") 
    elif os.path.isfile:
        print(f"Filename: {os.path.basename(path)}")
else:
    raise "incorrect path"