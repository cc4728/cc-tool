#!/bin/bash
# This is a tool for compiling and replacing the raspberry pi kernel
# Refs doc:https://www.raspberrypi.com/documentation/computers/linux_kernel.html
# author: jing.cai

# The path to the folder used to build the kernel
#workspace="./"
kernel_path="./linux/"

# The version number of kernel
kernel_version="rpi-5.10.y"

# The number of threads
thread_num="8"

# The path of sd card
boot_path="/dev/sdb1"
root_path="/dev/sdb2"

if [ "$1" == "-h" ] ; then
	echo "usage :"
	echo "	./kpi.sh init (at first time)"
	echo "	./kpi.sh make (build kernel)"
	echo "	./kpi.sh install (install the kernel by sd card)"
elif [ "$1" == "init" ]; then
	sudo rm -rf ${kernel_path}
# 1.Environment set up
## 1.1 install tools
	sudo apt install git bc bison flex libssl-dev make libc6-dev libncurses5-dev  &&

## 1.2 mkdir
#	mkdir ${workspace} &&
#	cd ${workspace} &&

# 2.Get kernel and toolchain from github
## 2.1 get kernel
	git clone --depth=1 -b ${kernel_version} https://github.com/raspberrypi/linux.git  &&

## 2.2 get toolchain
	sudo apt install crossbuild-essential-armhf &&
	cd ${kernel_path} &&
	
## 2.3 create path for install
	mkdir mnt &&
	mkdir mnt/fat32 &&
	mkdir mnt/ext4 
elif [ "$1" == "install" ]; then
	cd ${kernel_path}  &&
	KERNEL=kernel7l  &&
## 3.1 Mount
	sudo mount ${boot_path} mnt/fat32 &&
	sudo mount ${root_path} mnt/ext4  &&
	
	sudo env PATH=$PATH make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- INSTALL_MOD_PATH=mnt/ext4 modules_install  &&
	
	sudo cp mnt/fat32/$KERNEL.img mnt/fat32/$KERNEL-backup.img  &&
	sudo cp arch/arm/boot/zImage mnt/fat32/$KERNEL.img  &&
	sudo cp arch/arm/boot/dts/*.dtb mnt/fat32/  &&
	sudo cp arch/arm/boot/dts/overlays/*.dtb* mnt/fat32/overlays/  &&
	sudo cp arch/arm/boot/dts/overlays/README mnt/fat32/overlays/  &&
	sudo umount mnt/fat32 &&
	sudo umount mnt/ext4

elif [ "$1" == "make" ]; then
	cd ${kernel_path}  &&
## Default config,
	KERNEL=kernel7l  &&
	make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- bcm2711_defconfig  &&

## 3.2 DIY config
#make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- menuconfig

# 4.Compile the kernel and dts and modules 
# If you do not change the kernel version or modify the device information, you only need to compile the kernel separately.
	#make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- zImage -j${thread_num}
	#make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- modules -j${thread_num}
	#make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- dtbs
	make ARCH=arm CROSS_COMPILE=arm-linux-gnueabihf- zImage modules dtbs -j${thread_num}
else
	echo "usage :"
	echo "	./kpi.sh init (at first time)"
	echo "	./kpi.sh make (build full kernel)"
	echo "	./kpi.sh install (install the kernel by sd card)"
fi

