Build OpenCV package for Raspbian
=======================

## Requirements

1. Raspbian zipped image. You can download it from [here](https://downloads.raspberrypi.org/raspbian_latest)
2. OpenCV zipped sources from [github](https://github.com/Itseez/opencv/releases)
3. OpenCV modules cloned from [github](https://github.com/Itseez/opencv_contrib)
4. run __python setup.py__ with ***root***. This need for __fdisk__ and __mount__

## Before run **setup.py**

Copy downloaded opencv zipped sources and cloned additional modules into **opencv/**.
Raspbian image (zipped or unzipped) must exist into work directory where **setup.py** installed.

Working directory must have this hierarcy:
- raspbian.zip
- **opencv/**
    - 3.1.0.zip
    - **opencv_contrib/**
- README.md
- setup.py

## Run compiling & building

Login with root and simply run:
```sh
# python setup.py
```
> :exclamation: Compiling is a long process. Please be patient.

## Done

Compiled and builded opencv package will be stored in the working directory. Find the .deb file.

## List of references

1. https://wiki.debian.org/QemuUserEmulation
2. https://wiki.debian.org/RaspberryPi/qemu-user-static
3. http://neophob.com/2014/10/run-arm-binaries-in-your-docker-container-using-boot2docker/
4. https://github.com/dweinstein/dockerfile-qemu-arm-chroot
5. http://blog.jenrom.com/2014/09/14/%D1%83%D1%81%D1%82%D0%B0%D0%BD%D0%BE%D0%B2%D0%BA%D0%B0-opencv-%D0%BD%D0%B0-linux/
6. http://answers.opencv.org/questions/
7. http://elinux.org/RPi_Software
8. CrossCompiling:
    - https://wiki.debian.org/CrossToolchains
    - https://wiki.debian.org/ToolChain/Cross
    - http://docs.opencv.org/2.4/doc/tutorials/introduction/crosscompilation/arm_crosscompile_with_cmake.html
    - http://www.kitware.com/blog/home/post/426
