#!/bin/bash

if test '!' -f "`pwd`/src/antidote.plugin"
then
  echo "You must launch this script from the gedit-antidote root directory." >&2
  exit 255
fi

PROJECT_DIR=`pwd`
# GEDIT
GEDIT_SOURCE_DIR="$PROJECT_DIR/src"
GEDIT_DEST_DIR="$HOME/.local/share/gedit/plugins"

echo "PROJECT_DIR=$PROJECT_DIR"
echo "GEDIT_SOURCE=$GEDIT_SOURCE_DIR"
echo "GEDIT_DEST=$GEDIT_DEST_DIR"

if [ "$1" = "install" ]
then

  #
  # GEDIT
  #
  rm -rfv "$GEDIT_DEST_DIR/antidote"*

  mkdir -pv "$GEDIT_DEST_DIR/antidote/ui"
  mkdir -pv "$GEDIT_DEST_DIR/antidote/icons/24"
  mkdir -pv "$GEDIT_DEST_DIR/antidote/utils"

  ln -sv "$GEDIT_SOURCE_DIR/"*.plugin "$GEDIT_DEST_DIR/"
  ln -sv "$GEDIT_SOURCE_DIR/antidote/"*.py "$GEDIT_DEST_DIR/antidote/"
  ln -sv "$GEDIT_SOURCE_DIR/antidote/ui/"*.ui "$GEDIT_DEST_DIR/antidote/ui"
  ln -sv "$GEDIT_SOURCE_DIR/antidote/icons/24/"*.png "$GEDIT_DEST_DIR/antidote/icons/24"
  ln -sv "$GEDIT_SOURCE_DIR/antidote/utils/"*.py "$GEDIT_DEST_DIR/antidote/utils"

elif [ "$1" = "remove" ]
then
  #
  # GEDIT
  #
  rm -rfv "$GEDIT_DEST_DIR/antidote"
  rm -fv "$GEDIT_DEST_DIR/antidote.plugin"

else
  echo "`basename $0` install|remove" >&2
  exit 255
fi
