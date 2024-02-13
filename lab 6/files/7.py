with open("file_test.txt", 'r') as a:
    b = open("file_test1.txt", 'w')
    for line in a:
        b.write(line)
a.close()
b.close()