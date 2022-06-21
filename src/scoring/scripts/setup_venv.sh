#!/bin/bash
source ~/.bash_profile

# Passing the -r flag will delete and recreate the venv directory
while getopts "r" arg; do
  case $arg in
    r)
      echo Removing the venv
      rm -rf venv

      echo Recreating the venv
      python -m venv venv
      ;;
  esac
done

echo Activating the venv
if [ -d "venv/Scripts" ]; then
  . venv/Scripts/activate
elif [ -d "venv/bin" ]; then
  . venv/bin/activate
fi

echo Installing pip requirements
python -m pip install -r requirements.txt
