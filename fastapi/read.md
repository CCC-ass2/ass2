# Backend
FastAPI is used to send data to frontend.

## Structure
```
|- main.py
|- Dockerfile
|- config.json -- couchdb IP address
|- requirements.txt -- lib requirements
|- data_extraction.py -- function for extract data from couchdb
|- backup_page1/
  |- unemployment_rate_4GreaterCity.py -- for data process
|- backup_page2/
|- backup_page3/
  |- covid_analysis.py -- for data process
|- backup_page4/
```

## Run
```
$ cd fastapi
$ pip install -r requirements.txt

$ python run main.py
```
