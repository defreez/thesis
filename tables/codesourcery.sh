#!/bin/bash
# Builds nanddump in current directory
# Assumes Sourcery G++ Lite 2011.03-41 for ARM GNU/Linux downloaded
# Assumes Ubuntu 10.04 version of mtd-utils (20090606)

apt-get install ia32-libs build-essential
apt-get source mtd-utils
tar xvjf arm-2011.03-41-arm-none-linux-gnueabi-i686-pc-linux-gnu.tar.bz2
PATH=$PATH:`pwd`/arm-2011.03/bin
cp mtd-utils/nanddump.c .
cp -r mtd-utils-20090606/include .
arm-none-linux-gnueabi-gcc nanddump.c -o nanddump -static
