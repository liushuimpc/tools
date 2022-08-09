#!/bin/bash
printcolor() {
    printf "\033[1;33m[debugshell]\033[0m \033[1;32m[`date "+%Y-%m-%d %H:%M:%S"`]\033[0m \033[1;31m$*\n\033[0m"
}

systemconfig=`ls device/mediatek/system |grep mssi*`

product="p1"
build_session="full"
build_type="user"
gms_version="yes"
otapackage=" "
thread=10

for i in $*
do
    if [ $i == "p1" ]; then
        product=p1
    elif [ $i == "p2" ]; then
        product=p2
    fi

    if [[ $i == "full" ]]; then
        build_session=full
    elif [[ $i == "sys" || $i == "system" ]]; then
        build_session=sys
    elif [[ $i == "vnd" || $i == "vendor" ]]; then
        build_session=vnd
    elif [[ $i == "package" ]]; then
        build_session=package
    fi

    if [[ $i == "userdebug" || $i == "ud" || $i == "debug" ]]; then
        build_type=userdebug
    elif [[ $i == "user" ]]; then
        build_type=user
    elif [[ $i == "eng" ]]; then
        build_type=eng
    fi

    if [[ $i == "gms" ]]; then
        gms_version=yes
    elif [[ $i == "aosp" ]]; then
        gms_version=no
    fi

    if [[ $i == "ota" ]]; then
        otapackage=--otapackage
    fi

    # Get a number as build thread number
    expr $i + 0 &>/dev/null
    if [[ $? == "0" ]]; then
        thread=$i
    fi
done

echo "product       = "$product
echo "build_session = "$build_session
echo "build_type    = "$build_type
echo "gms_version   = "$gms_version
echo "otapackage    = "$otapackage
echo "thread        = "$thread

if [[  "$build_session" == "full" ]]; then
    printcolor "---------double build sytem and build ---------"
    printcolor "---------start build system---------"
    source build/envsetup.sh
    export OUT_DIR=out_sys
    lunch sys_$systemconfig-"$build_type"
    make sys_images BUILD_GMS=$gms_version -j$thread    
    if [ $? != 0 ];then
        printcolor "system build fail,please check"
        exit 1
    fi

    printcolor "-------start build vendor-----"
    source build/envsetup.sh
    export OUT_DIR=out_vnd
    lunch $product-"$build_type"
    make vnd_images krn_images  BUILD_GMS=$gms_version -j$thread
    if [ $? != 0 ];then
        printcolor "vendor build fail,please check"
        exit 1
    fi
    printcolor "-------start android image-----"
    python out_sys/target/product/$systemconfig/images/split_build.py \
        --system-dir out_sys/target/product/$systemconfig/images \
        --vendor-dir out_vnd/target/product/$product/images \
        --kernel-dir out_vnd/target/product/$product/images \
        --output-dir out/target/product/$product/ $otapackage

elif [[  "$build_session" == "sys"  ]]; then
    printcolor "-------only build system---------"
    source build/envsetup.sh
    export OUT_DIR=out_sys
    lunch sys_$systemconfig-"$build_type"
    make sys_images BUILD_GMS=$gms_version -j$thread
    if [ $? != 0 ];then
        printcolor "system build fail,please check"
        exit 1
    fi

elif [[ "$build_session" == "vnd"  ]]; then
    printcolor "-------only build vendor---------"
    source build/envsetup.sh
    export OUT_DIR=out_vnd
    lunch $product-"$build_type"
    make vnd_images krn_images BUILD_GMS=$gms_version -j$thread
    if [ $? != 0 ];then
        printcolor "vendor  build fail,please check"
        exit 1
    fi

elif [[ "$build_session" == "package"  ]]; then
    printcolor "-------start android image-----"
    python out_sys/target/product/$systemconfig/images/split_build.py \
        --system-dir out_sys/target/product/$systemconfig/images \
        --vendor-dir out_vnd/target/product/$product/images \
        --kernel-dir out_vnd/target/product/$product/images \
        --output-dir out/target/product/$product/ $otapackage 
    if [ $? != 0 ]; then
        printcolor "package build fail,please check"
        exit 1
    else
        printcolor "package successfully"
        exit 1
    fi
fi
