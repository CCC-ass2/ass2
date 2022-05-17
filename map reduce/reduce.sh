# bin/bash

npm install
echo "npm install finish"

export dbname1="au_covid"
#export dbname2="au_employment"
export dbname3="au_main"
grunt couch-compile
grunt couch-push
echo "map reduce compile finish"

# sentiment
for i in {1..3}
do
  curl -XGET "http://admin:admin@172.26.133.30:5984/au_covid/_design/language/_view/sentiment?reduce=true&group_level=$i" \
  > "result/covid/sentiment/reduce$i.json"
done

for i in {1..3}
do
  curl -XGET "http://admin:admin@172.26.133.30:5984/au_covid/_design/language/_view/city_time?reduce=true&group_level=$i" \
  > "result/covid/city_time/reduce$i.json"
done

# employment
for i in {1..4}
do
  curl -XGET "http://admin:admin@172.26.133.30:5984/au_main/_design/language/_view/date_time?reduce=true&group_level=$i" \
  > "result/employment/datetime/reduce$i.json"
done

for i in {1..4}
do
  curl -XGET "http://admin:admin@172.26.133.30:5984/au_main/_design/language/_view/week_time?reduce=true&group_level=$i" \
  > "result/employment/weektime/reduce$i.json"
done

# stress
curl -XGET "http://admin:admin@172.26.133.30:5984/au_main/_design/language/_view/text?reduce=false" > "result/stress/text.json"