#!/bin/bash

docker rmi vfiftyfive/marvel_init_db -f
docker buildx build --platform linux/amd64,linux/arm64 --push -t vfiftyfive/marvel_init_db .
docker run --env API_PRIVATE_KEY="2ff768c5567a1e2035dcef735e2be04e7af86daa" --env MONGO_HOST="172.17.0.2" -d vfiftyfive/marvel_init_db
