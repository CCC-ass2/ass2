# CCC Assignment 2

## Video

## Structure
```
|- Ansbile -- deployment
|- twitterAPI -- data wrangling
|- fastapi -- backend
|- streamlit -- frontend
|- run.sh -- set up
```

## Architecture
![alt text](https://github.com/CCC-ass2/ass2/blob/main/Image/architecture.png)

## Deployment user guide

#### 1. Deploy instances on MRC with Ansible playbook
```
$ git clone https://github.com/CCC-ass2/ass2  
$ cd Ansible
$ ./run-nectar.sh
```
#### 2. Set up distributed CouchDB with docker container 
```
$ ./docker_db.sh
```
#### 3.	Set up CouchDB cluster in Master node
```
$ ./db_cluster.sh
```

#### 4. Backend & Frontend
```
$ bash run.sh
```

## Issues
### 1. MRC issues
As all of our groupmates are in China, we have to use VPN to connect to MRC. That leads to a big issue. Many times we can not get access to instances. Also, at last we deploy our frontend on the instance, but we can't get access to the web link. We are not sure it is a problem of port setting up or using the intranet of MRC. Therefore, although we deploy it on MRC, we still afraid that the user will not be able to visit it. Here we offer another option to the users.

At directory /streamlit, it contains all things we need to set up the webpages. As I mention in the report, due to the efficiency consideration, the processed data is stored into each /pages/backup_page[i]/data.json. The data.json is updated to the most recent data before the due day. Therefore, if the user want to see the result, just feel free to download the /streamlit file (and only this one!!), follow the step below.

```
# go to the streamlit file
$ cd streamlit

# run
$ bash run_without_delete.sh
```

Then you will see the result!
