
# This initialization step is required to run on each of the instance to create CouchDB

# install docker
sudo api update
sudo apt install docker
sudo apt install docker.io

# docker group
groupadd docker
sudo gpasswd -a ubuntu docker
newgrp docker
sudo service docker restart
newgrp – docker

# define environmental variable
export declare nodes=( 172.26.xxx.xxx) #recommended to be same as server ip
export masternode=`echo ${nodes} | cut -f1 -d' '`
export declare othernodes=`echo ${nodes[@]} | sed s/${masternode}//`
export size=${#nodes[@]}
export user='admin'
export pass='admin'
export VERSION='3.0.0'
export cookie='a192aeb9904e6590849337933b000c99'

# get all docker images
docker pull couchdb:${VERSION}

# stop and remove existing docker container
for node in "${nodes[@]}" 
  do
    if [ ! -z $(docker ps --all --filter "name=couchdb${node}" --quiet) ] 
       then
         docker stop $(docker ps --all --filter "name=couchdb${node}" --quiet) 
         docker rm $(docker ps --all --filter "name=couchdb${node}" --quiet)
    fi 
done

# create container, open ports for distributed cluster communication
for node in "${nodes[@]}" 
  do
    docker create\
      -p 9100:9100\
      -p 4369:4369\
      -p 5984:5984\
      --name couchdb${node}\
      --env COUCHDB_USER=${user}\
      --env COUCHDB_PASSWORD=${pass}\
      --env COUCHDB_SECRET=${cookie}\
      --env ERL_FLAGS="-setcookie \"${cookie}\" -name \"couchdb@${node}\""\
      couchdb:${VERSION}
done

# create docker id variable
declare -a conts=(`docker ps --all | grep couchdb | cut -f1 -d' ' | xargs -n${size} -d'\n'`)

# Start and run docker container
for cont in "${conts[@]}"; do docker start ${cont}; done
