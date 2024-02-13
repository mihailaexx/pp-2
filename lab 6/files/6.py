import string
for letter in list(string.ascii_uppercase):
    open(f"alphabet/{letter}.txt", 'x') # использовал папку чтобы не засорять основную директорию