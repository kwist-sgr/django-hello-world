#!/bin/bash

MANAGE=django-admin.py
OUTPUT_FILE=`date +"%Y-%m-%d"`.dat

PYTHONPATH=`pwd` DJANGO_SETTINGS_MODULE=django_hello_world.settings $MANAGE print_all_models 2> $OUTPUT_FILE
