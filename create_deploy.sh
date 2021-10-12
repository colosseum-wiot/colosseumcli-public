#!/usr/bin/env bash

PROJECT_NAME=colosseumcli

#clean
rm -rf $PROJECT_NAME.tar.gz  build dist $PROJECT_NAME.egg-info wheels

python setup.py sdist
python setup.py bdist_wheel

pip wheel -e . -w wheels

#tar -czvf srn-controller-wheels.tar.gz wheels/*

#tar -czvf srn-controller.tar.gz srn-controller-wheels.tar.gz utility/startSrnCtrl.sh config/competitor_profile.yaml config/test_competitor_profile.yaml install_files/*

#clean
rm -rf  build $PROJECT_NAME.egg-info 
