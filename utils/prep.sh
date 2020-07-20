#!/bin/sh
###
# Simple Shell script to configure settings.
###

MV=mv

cd ~

git clone https://github.com/gitvipin/pandora.git

$MV .vimrc .vimrc.orig
$MV .bashrc .bashrc.orig
$MV .screenrc .screenrc.orig
$MV .gitconfig .gitconfig.orig
$MV .aliases .aliases.orig

ln -s ~/pandora/init/vimrc .vimrc
ln -s ~/pandora/init/bashrc .bashrc
ln -s ~/pandora/init/screenrc .screenrc
ln -s ~/pandora/init/gitconfig .gitconfig
ln -s ~/pandora/init/aliases .aliases
ln -s ~/pandora/init/init.py ~/.init.py
ln -s ~/pandora/init/login .

touch ~/.aliases_local
echo "Created dummy .aliases_local file. Overwrite it if needed."
