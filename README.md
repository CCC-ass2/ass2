# CCC Assignment 2

## Video

![alt text](https://github.com/CCC-ass2/ass2/blob/main/Image/aboutus.jpg)

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

#### 4. map reduce
```
# Assume the user is in ass2 directory
$ cd map_reduce
$ bash reduce.sh
```

#### 4. Backend & Frontend
```
# This will install all dependencies and run the backend
# Assume the user is in ass2 directory
$ bash run.sh

# For frontend, please go to another terminal as the last one will be occupied by the backend
# Assume the user is in ass2 directory
$ cd streamlit
$ bash run.sh   # for deleting the stored data
$ bash run_without_deletion.sh    # for not deleting the stored data
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

But we still run it on MRC, here is the running interface.

fastapi running...

![alt text](https://github.com/CCC-ass2/ass2/blob/main/Image/fastapirun_on_mrc.jpg)

streamlit running...

![alt text](https://github.com/CCC-ass2/ass2/blob/main/Image/strun_on_mrc.jpg)

### 2. Docker
At the beginning,  our group hope to deploy backend and frontend by docker and on two different instances. However, due to the intranet issues, most of time we can't access two instances at the same time, thus we can't try how to deploy it. Also, it is hard for us to figure out the IP adress in such situation. Therefore, at last we just deploy it on the instance without containerize them. However, the Dockerfile is programmed and for backend it is at `ass2/fastapi/Dockerfile`, for frontend it is at `ass2/streamlit/Dockerfile`. If the user want to try, please try it. The only thing need to be mentioned is the IP address should be changed when using docker. In `ass2/fastapi/config.json`, it stores the IP Address for couchDB; in `ass2/streamlit/config.json`, it stores the IP Address of backend. So it needs to be figured out by backend(fastapi) docker.

### 3. Force to use two terminals to deploy backend and frontend
This issue exists as the terminal will be occupied and showing error information when backend/frontend running. An example is shown as follows.

fastapi running...

![alt text](https://github.com/CCC-ass2/ass2/blob/main/Image/fastapirun.jpg)

streamlit running...

![alt text](https://github.com/CCC-ass2/ass2/blob/main/Image/strun.jpg)


We assume this issue can be solved by containize them into docker, thus the running and error information will be shown in the container. However, as what we mentioned before, we are not able to containize it thus leacing this issue.
