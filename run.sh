#!/usr/bin/env bash

sudo apt-get install python3.8
sudo apt-get install python3-pip

#rm pages/backup_page1/data.json
#rm pages/backup_page2/data.json
#rm pages/backup_page3/data.json

pip install -r streamlit/requirements.txt
pip install -r fastapi/requirements.txt
echo "environment set up finish"

cd fastapi
python main.py

cd ..
cd streamlit
streamlit run main.py
