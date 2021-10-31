#!/bin/bash

docker rmi vfiftyfive/flask_marvel -f
docker buildx build --platform linux/amd64,linux/arm64 --push -t vfiftyfive/flask_marvel .
docker run -p 80:80 vfiftyfive/flask_marvel

