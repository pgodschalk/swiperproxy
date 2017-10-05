#!/bin/bash

set -e

cd $(dirname $0)

IMAGE="swiperproxy/swiperproxy"

docker build -t $IMAGE -f Dockerfile ..
