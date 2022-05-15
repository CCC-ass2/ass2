#!/usr/bin/env bash

sudo apt-get install python3.8
sudo apt-get install python3-pip

bash fastapi/run.sh
bash streamlit/run.sh