import os
import subprocess

# you have to run this file only one time
paths = ['/Users/alex/memes/memesworldclass', '/Users/alex/memes/pcixoff']  # you have to change the path
os.chdir('/Users/alex/memes')  # you have to change the path
subprocess.run(['instaloader memesworldclass'], shell=True)
subprocess.run(['instaloader pcixoff '], shell=True)


def remove_files(path):
    os.chdir(path)
    for i in os.listdir():
        if os.path.splitext(i)[1] != '.jpg':
            os.remove(i)


for path in paths:
    remove_files(path)
