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
