#!/usr/bin/env bash

set -e

source subd_venv/bin/activate
python3 subd_parser.py -i rk1_questions.txt -d rk1 --no-title
python3 subd_parser.py -i rk2_questions.txt -d rk2 --no-title

