#!/usr/bin/env python3
#
# Author: Marco Li<marco.li@datalogic.com>
#
# Usage
#     python getApkInfo.py                      # Get apk information under current directory
#     python getApkInfo.py [dir1|dir2|...]      # Get apk information for specify directories

import os
import sys
import zipfile
import re

def getAppBaseInfo(apkName, apkpath):
    output = os.popen("aapt d badging %s" % apkpath).read()
    print("===================%s===================" % apkName)
    print(output + "\n")

def isApk(path):
    suffix = path.rsplit(".")
    if (suffix[len(suffix) - 1] == "apk"):
        return True
    else:
        return False

def walkFile(path):
    for root, dirs, files in os.walk(path):
        for f in files:
            if (isApk(f)):
                getAppBaseInfo(f, os.path.join(root, f))

def main():
    length = len(sys.argv)

    if length == 1:
        walkFile("./")
    elif length > 1:
        for argv in sys.argv:
            walkFile(argv)

if __name__ == "__main__":
    main()
