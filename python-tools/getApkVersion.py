#!/usr/bin/env python3
#
# Author: Marco Li<marco.li@datalogic.com>
#
# Usage
#     python getApkVersion.py                      # Get apk versions under current directory
#     python getApkVersion.py [dir1|dir2|...]      # Get apk versions for specify directories

import os
import sys
import zipfile
import re

def getAppBaseInfo(apkName, apkpath):
    output = os.popen("aapt d badging %s" % apkpath).read()
    # print('OUTPUT:' + output)
    match = re.compile("package: name='(\S+)' versionCode='(\d+)' versionName='(.*?)'").match(output)
    if not match:
        print("\n%s can't get packageinfo\n" % apkName)
        return

    packageName = match.group(1)
    versionCode = match.group(2)
    versionName = match.group(3)

    # print('packageName: ' + packageName)
    # print('versionCode: ' + versionCode)
    # print('versionName: ' + versionName)
    pureName = apkName.rsplit(".")[0]
    print('%-45.45s %25s' %(pureName, versionName))

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
