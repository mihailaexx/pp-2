with open("output.txt", 'r') as a:
    b = open("file_test1.txt", 'w')
    for line in a:
        b.write(line)