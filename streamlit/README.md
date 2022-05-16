# Frontend

This program uses streamlit as the fronend.

## Structure
```
|- main.py
|- backup_main.py
|- Dockerfile
|- config.json -- backend IP address
|- requirements.txt -- lib requirements
|- run.sh -- automation deployment
|- page/
   |- page0.py
   |- page1.py
   |- page2.py
   |- page3.py
   |- backup_page1/
      |- Data/ -- data to store with code
      |- data.json -- data to extract from backend
      |- dataprocess.py -- data processing function for page1
   |- backup_page2/
      |- data.json -- data to extract from backend
   |- backup_page3/
      |- Data/ -- data to store with code
      |- data.json -- data to extract from backend
   |- backup_page4/
```

## Run
```
###### with python3.8
$ cd streamlit    # enter file
$ pip install -r requirements.txt

# There are two ways to run. Data are extracted from backend and store in the code as the consideration of 
# efficiency. Therefore, if the user don't want to update the data, can directly run by:
$ streamlit run main.py   # default port is 8051, for using other port, run streamlit run main.py --server.port [port]

# The other way is remove all data and extract from backend by:
$ bash run.sh
```

