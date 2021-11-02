#!/bin/bash

docker rmi vfiftyfive/marvel_init_db -f
docker buildx build --platform linux/amd64,linux/arm64 --push -t vfiftyfive/marvel_init_db .
docker run --env MONGO_HOST="172.17.0.4" -d vfiftyfive/marvel_init_db
