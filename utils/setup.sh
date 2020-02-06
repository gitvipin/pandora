#!/bin/sh
# Modifies Aliases locallly.
mv .bashrc .bashrc.old
mv .vimrc .vimrc.old
mv .screenrc .screenrc.old
mv .gitconfig .gitconfig.old
ln -s /root/pandora/init/aliases  .aliases
ln -s /root/pandora/init/vimrc .vimrc
ln -s /root/pandora/init/gitconfig .gitconfig
ln -s /root/pandora/init/bashrc .bashrc
ln -s /root/pandora/init/screenrc .
ln -s /root/neel/init/aliases_local .aliases_local
