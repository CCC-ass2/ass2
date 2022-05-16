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
$ bash run_without_deletion.sh   # default port is 8051, for using other port, run streamlit run main.py --server.port [port]

# The other way is remove all data and extract from backend by:
$ bash run.sh
```

## Note
If you just want to update the data, use the following steps.

1. Start backend by intructions in /fastapi
2. Extract data from fastapi
```
# data for page1
$ curl -XGET "http://127.0.0.1:8000/page1data"

# data for page2
$ curl -XGET "http://127.0.0.1:8000/page2data"

# data for page3
$ curl -XGET "http://127.0.0.1:8000/page3data"
```
3. store data
-- store page1data to pages/backup_page1/data.json
-- store page2data to pages/backup_page2/data.json
-- store page3data to pages/backup_page3/data.json
Then start frontend.
