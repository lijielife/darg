#!/bin/bash
set -xe

if [ ! -d "scripts" ]; then
  echo 'this script must be executed from project root'
fi

#get highest tag number
VERSION=`git describe --abbrev=0 --tags`

#replace . with space so can split into an array
VERSION_BITS=(${VERSION//./ })

if [ "$1" ]; then
    NEW_TAG=$1
else
    #get number parts and increase last one by 1
    VNUM1=${VERSION_BITS[0]}
    VNUM2=${VERSION_BITS[1]}
    VNUM3=${VERSION_BITS[2]}
    VNUM3=$((VNUM3+1))
    NEW_TAG="$VNUM1.$VNUM2.$VNUM3"
fi

echo "Updating $VERSION to $NEW_TAG"

#get current hash and see if it already has a tag
GIT_COMMIT=`git rev-parse HEAD`
NEEDS_TAG=`git describe --contains $GIT_COMMIT`

#only tag if no tag already (would be better if the git describe command above could have a silent option)
if [ -z "$NEEDS_TAG" ]; then
    echo "Tagged with $NEW_TAG (Ignoring fatal:cannot describe - this means commit is untagged) "
    git tag $NEW_TAG
    git push --tags
    # updating base.py
    echo "updating app version..."
    sed -i "s/VERSION = '.*'/VERSION = '$NEW_TAG'/g" site/project/settings/base.py
    echo "file says now:"
    grep "VERSION" site/project/settings/base.py
    echo "commiting file..."
    git add site/project/settings/base.py && git commit -m "updated version at base.py to $NEW_TAG" && git push
    ID=`git log --format="%H" -n 1`
    git checkout develop
    git cherry-pick $ID
    git checkout master
    echo "done"
else
    echo "Already a tag on this commit"
fi
