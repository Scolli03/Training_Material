import os
from collections import OrderedDict

curDir = os.getcwd()
print(curDir + "\\filepath.txt")
file = open(curDir + "\\filepath.txt", "r")
print(file.read())
directory = file.read()
os.chdir(directory)
directory_info = {}
convertedDict = {}
kilobyte = 1024
megabyte = 1048576
gigabyte = 1073741824


def absoluteFilePaths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            try:
                fp = os.path.join(dirpath, f)
                total_size += os.path.getsize(fp)
            except Exception as e:
                print(e)
    return total_size


def convertSize(bytes):
    sizeInBytes = bytes[0]
    try:
        if sizeInBytes < kilobyte:
            fileSize = str(sizeInBytes) + " Bytes"
        elif sizeInBytes < gigabyte and megabyte > sizeInBytes > kilobyte:
            fileSize = str(round(sizeInBytes / kilobyte)) + " KB"
        elif sizeInBytes < gigabyte and sizeInBytes >= megabyte:
            fileSize = str(round(sizeInBytes / megabyte)) + " MB"
        elif sizeInBytes >= gigabyte:
            fileSize = str(round(sizeInBytes / gigabyte)) + " GB"
    except ZeroDivisionError as e:
        fileSize = "Not Calculable"
    return fileSize


for dir in os.listdir(directory):
    path = os.path.abspath(os.path.join(dir))
    print(path)
    sizeInBytes = get_size(path)
    directory_info[dir] = [sizeInBytes]

dict_sorted_keys = sorted(directory_info, key=directory_info.get, reverse=True)
print(dict_sorted_keys)
for dir in dict_sorted_keys:
    print(dir)
    print(directory_info[dir])
    convertedDict[dir] = [convertSize(directory_info[dir])]
for r in convertedDict:
    print(r, convertedDict[r])
with open(r'C:\Users\Shain\Desktop\sizes.txt', 'w') as f:
    f.write("Program (file size)\n\n")
    for r in convertedDict:
        line = "{} ({})\n".format(r, str(convertedDict[r][0]))
        f.write(line)
