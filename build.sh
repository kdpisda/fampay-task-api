#!/bin/bash
# branch=`git rev-parse --abbrev-ref HEAD`
# image_tag="v0.$(git rev-list --count ${branch}).${branch:0:3}.$(git rev-parse --short HEAD)"
image_tag=v0.1

echo "build_number=$image_tag"

imageName=fampay/api:$image_tag

echo "Building Image $imageName"

docker build -t $imageName -f Dockerfile  .

if [ $? -eq 0 ]; then
   echo "Image built $imageName"
else
   echo "Unable to build $imageName"
fi

echo "build_number=$image_tag"