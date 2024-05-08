#!/bin/bash

# Create docker network0
if [ $( docker network ls | grep echofeed | wc -l ) -eq 0 ]; then
  docker network create echofeed
fi

# Start services
start_service () {
  docker stop echofeed-"$1" && docker rm echofeed-"$1"
  docker rmi echofeed-"$1"

  docker build -f echofeed/"$1"/Dockerfile_"$1" -t echofeed-"$1" .

  docker run --net echofeed -p "$2":"$2" --name echofeed-"$1" echofeed-"$1" &
}

start_service api 8080


# Elasticsearch
if [ $( docker ps -a | grep echofeed-elastic | wc -l ) -gt 0 ]; then
  docker start echofeed-elastic
else
  docker run --net echofeed --name echofeed-elastic -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" -e "xpack.security.enabled=false" docker.elastic.co/elasticsearch/elasticsearch:8.11.4 &
fi


# Testing
set -x

SCRIPT_PATH=$(dirname "$0")

python -m pylint echofeed \
  --init-hook="import sys; sys.path.append('$SCRIPT_PATH')" \
  --rcfile=.pylintrc

python -m pytest --disable-warnings --no-warn-script-locationS