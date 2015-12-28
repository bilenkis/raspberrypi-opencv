#/usr/bin/python
import os
import re
import sys
from subprocess import Popen, PIPE, check_output

def imgprocessing( img ):
    # get offset for mount
    p = check_output(['fdisk','-lu', img])
    m = re.search("\.img2\s+(\d+)\s+", p)
    offset = int(m.group(1)) * 512
    # mount img
    cmd = "mount -o loop,ro,offset=" + str(offset) + " " + img + " " + "mnt/"
    p = Popen([cmd], shell=True)
    p.wait()
    # copy to chroot
    p = Popen(['rsync -a mnt/ chroot/'], shell=True)
    p.wait()
    p = Popen(['umount mnt/'], shell=True)
    p.wait()
    cmd = 'rsync -a opencv/' + "'" + opencvfile + "' " + 'chroot/usr/src/'
    p = Popen([cmd], shell=True)
    p.wait()
    p = Popen(['rsync -a opencv/opencv_contrib chroot/usr/src/'], shell=True)
    p.wait()
    # chroot & run build
    ldsofile = 'chroot/etc/ld.so.preload'
    p = Popen(['test', '-e', ldsofile])
    p.wait()
    if not p.returncode:
        p = Popen(['rm', ldsofile])
        p.wait()
    p = Popen(['cp -rp /usr/bin/qemu-arm-static chroot/usr/bin/'], shell=True)
    p.wait()
    p = Popen(['chroot chroot/ /bin/bash -c "set -xe \
                                            && apt-get update  \
                                            && apt-get install -y \
                                                    git \
                                                    make \
                                                    cmake \
                                                    libjpeg-dev \
                                                    libtiff5-dev \
                                                    libjasper-dev \
                                                    libgtk2.0-dev \
                                                    libavcodec-dev \
                                                    libavformat-dev \
                                                    libswscale-dev \
                                                    libv4l-dev \
                                                    libdc1394-22-dev \
                                                    libxine2-dev \
                                                    libgstreamer0.10-dev \
                                                    libgstreamer-plugins-base0.10-dev \
                                                    libqt4-dev \
                                            "'], shell=True)
    p.wait()
    cmd = 'chroot chroot/ /bin/bash -c "set -xe \
                                            && cd /usr/src \
                                            && mkdir ' + opencvfile + '/build \
                                            && cd ' + opencvfile + '/build \
                                            && cmake -DCMAKE_TOOLCHAIN_FILE=../platforms/linux/arm-gnueabi.toolchain.cmake \
                                                    -DCMAKE_C_COMPILER=/usr/bin/arm-linux-gnueabihf-gcc \
                                                    -DCMAKE_CXX_COMPILER=/usr/bin/arm-linux-gnueabihf-c++ \
                                                    -D OPENCV_EXTRA_MODULES_PATH=../opencv_contrib/modules \
                                                    -D CMAKE_BUILD_TYPE=RELEASE \
                                                    -D WITH_TBB=ON \
                                                    -D BUILD_NEW_PYTHON_SUPPORT=ON \
                                                    -D WITH_V4L=ON \
                                                    -D INSTALL_PYTHON_EXAMPLES=ON \
                                                    -D BUILD_EXAMPLES=ON \
                                                    -D WITH_OPENGL=ON \
                                                    .. \
                                            && make -j$(nproc)\
                                            && checkinstall -y -D -A armhf \
                                                    --install=no \
                                                    --nodoc \
                                                    --maintainer=adm@bilenkis.ru \
                                                    --pkgname=opencv \
                                                    --pkgversion=' + opencv_version + ' \
                                                    --backup=no \
          "'
    print "make: [%s]" % cmd
    p = Popen([cmd], shell=True)

# check opencv
if len(sys.argv) < 2:
    print "1. Download opencv into dir [opencv/] like:\n" \
            "\t [dir: opencv/]# curl -OLv https://github.com/Itseez/opencv/archive/3.1.0.zip\n" \
            "2. Clone opencv modules into dir [opencv/opencv_contrib] like:\n" \
            "\t [dir: opencv/]# git clone https://github.com/Itseez/opencv_contrib\n" \
            "3. Run this setup.py once again with 'OK':\n" \
            "\t # python setup.py OK\n"
    exit(1)

if sys.argv[1] != "OK":
    print "You must run: python setup.py OK"
    exit(1)

# unzip opencv
os.chdir("opencv")
zipfile = ''
for line in os.listdir("."):
    if re.search("\.zip$",line):
        zipfile = line

if len(zipfile):
    m = re.search("(.+)\.zip$", zipfile)
    opencv_version = m.group(1)
    opencvfile = check_output(['unzip','-Z','-1', zipfile])
    m = re.search('(.+)/',opencvfile)
    opencvfile = m.group(1)
    print "Extract to opencv/%s" % opencvfile
    p = check_output(['unzip', '-u', zipfile ])
os.chdir("..")

# check qemu
p = Popen(['test -e /usr/bin/qemu-arm-static'], shell=True)
p.wait()
if p.returncode:
    print "Not found: /usr/bin/qemu-arm-static\nInstall it first like:\n" \
            "apt-get install qemu qemu-user-static binfmt-support\n"
    exit(1)

# check RPi .zip | .img files
imgfile, zipfile = ('', '')
for line in os.listdir("."):
    if re.search("\.img$",line):
        imgfile = line
    elif re.search("\.zip$",line):
        zipfile = line

if len(imgfile):
    print "Found RPi .img"
    imgprocessing(imgfile)
if len(zipfile) and not len(imgfile):
    print "Found RPi .zip"
    unzipfile = check_output(['unzip','-Z','-1', zipfile ])
    print "Extract to %s" % unzipfile
    p = check_output(['unzip', '-u', zipfile ])
    imgprocessing(unzipfile)
if not len(imgfile) and not len(zipfile):
    print "Not found any .zip or .img file in image/. Exit."
    exit(1)
