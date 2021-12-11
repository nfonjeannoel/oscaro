# Python program to explain os.mkdir() method

# importing os module
import os
from random import randint
# Directory
directory = "DownloadedText"

# Parent Directory path
parent_dir = "C:/Users/JEANNOEL/PycharmProjects/oscaro"

# Path
path = os.path.join(parent_dir, directory)

try:
    os.makedirs(path, exist_ok = True)
    print("Directory '%s' created successfully" % directory)

except OSError as error:
    print("Directory '%s' can not be created, it already exist" % directory)

