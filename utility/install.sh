#!/bin/bash

packages='nmap hydra'

if [ -x "$(command -v apt-get)" ];then sudo apt-get install $packages
elif [ -x "$(command -v pacman)" ];then sudo pacman -S $packages
elif [ -x "$(command -v apk)" ];then sudo apk add --no-cache $packages
elif [ -x "$(command -v dnf)" ];then sudo dnf install $packages
elif [ -x "$(command -v yum)" ];then sudo yum install $packages
elif [ -x "$(command -v yay)" ];then sudo yay -S $packages
else [ -x "$(command -v zypper)" ] sudo zypper install $packages
fi
