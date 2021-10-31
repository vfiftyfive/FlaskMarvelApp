#!/bin/bash

docker rmi vfiftyfive/marvel_init_db -f
docker buildx build --platform linux/amd64,linux/arm64 --push -t vfiftyfive/marvel_init_db .
docker run -d vfiftyfive/marvel_init_db
