#! /bin/bash
IMAGE='burudoza:latest'
CONTAINER='burudoza'
PORT=8501

docker rmi -f $IMAGE | docker build -t $IMAGE .
docker container prune -f
docker run -p $PORT:$PORT --name $CONTAINER $IMAGE
# docker run -it --name $CONTAINER $IMAGE

