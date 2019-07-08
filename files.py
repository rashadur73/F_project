#f = open('demo.txt', mode = 'r')
#f.write('Bismillahir Rahmanir Rahim')
#file_content = f.read()
#f.write('  MashaAllah\n')

# file_content = f.readlines()
# f.close()

# print(file_content)

# for line in file_content:
#     print(line[:-1])
with open('demo.txt',mode = 'r') as f:
    line = f.readline()
    while line :
        print(line)
        line = f.readline()
