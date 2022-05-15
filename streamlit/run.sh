#!/usr/bin/env bash

rm pages/backup_page1/data.json
rm pages/backup_page2/data.json
rm pages/backup_page3/data.json

echo "All history data is deleted"

echo "Run frontend"
#streamlit run main.py