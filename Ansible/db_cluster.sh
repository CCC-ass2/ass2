
# This script only need to run on master node (i.e. 172.26.134.227), replace "172.26.130.179" with node's ip adddress that is required to added to the cluster
# Distributed Cluster set-up 

curl -X POST -H "Content-Type: application/json" http:// ${user}:${pass}@172.26.134.227:5984/_cluster_setup -d '{"action": "enable_cluster", "bind_address":"0.0.0.0", "username": "admin", "password":"admin", "port": 5984, "node_count": "3", "remote_node": "172.26.130.179", "remote_current_user": "admin", "remote_current_password": "admin" }'

curl -X POST -H "Content-Type: application/json" http:// ${user}:${pass}@172.26.134.227:5984/_cluster_setup -d '{"action": "add_node", "host":"172.26.130.179", "port": 5984, "username": ${user}, "password":${pass}}'
