#!/bin/bash
set -e

function read_version() {
  VERSION=`cat .version`
}
read_version
IMAGE_NAME='stock-prediction'
echo  "Build [${IMAGE_NAME}] image - version : ${VERSION}"

docker build --tag ${IMAGE_NAME}:${VERSION} .
