#!/bin/sh
# Modifies Aliases locallly.
mv .bashrc .bashrc.old
mv .vimrc .vimrc.old
mv .screenrc .screenrc.old
mv .gitconfig .gitconfig.old
ln -s ~/pandora/init/aliases  .aliases
ln -s ~/pandora/init/vimrc .vimrc
ln -s ~/pandora/init/gitconfig .gitconfig
ln -s ~/pandora/init/bashrc .bashrc
ln -s ~/pandora/init/screenrc .screenrc
ln -s ~/pandora/init/init.py .init.py
touch .aliases_local
