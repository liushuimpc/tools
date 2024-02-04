# tools

Simple tools


## Description
### repo-relevant-tools/local.xml
- A local manifest xml, it can replace some of your private projects in a huge group.

### jenkins/remove-specific-builds.sh
- The script to remove specific builds in Jenkins, to clean up the space.

### jenkins/
- getApkInfo.py                             # Get apk information under current directory
- python getApkInfo.py [dir1|dir2|...]      # Get apk information for specify directories

### rsa-keys
- The method to generate key, encrypt and decrypt......


## Usage
### dl_private.xml
1. copy dl_private.xml to $M11_A13_AOSP/.repo/local_manifests/.
2. Use below command to synchronize your M11_A13_AOSP for first time.
```
$ repo sync --force-sync
```
3. After the first time force sync success in your local, your can use generic way to synchrnoize as usual.
```
$ repo sync
```

### getApkInfo.py
1. python getApkInfo.py                      # Get apk information under current directory

### getApkInfo.py
1. python getApkInfo.py [dir1|dir2|...]      # Get apk information for specify directories

