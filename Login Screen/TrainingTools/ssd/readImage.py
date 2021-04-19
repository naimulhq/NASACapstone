import os
cwd = os.getcwd()
cwd = cwd + "/JPEGImages"
files = []
for _,_,filenames in os.walk(cwd):
    files.append(filenames)

f = open("train.txt","w+")
for i in filenames:
    f.write(i[0:len(i)-4] +"\n")
f.close()
