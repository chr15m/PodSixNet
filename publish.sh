#!/bin/sh

BZRREV=`bzr log -r -1.. --line | cut -d":" -f 1`
SRV=mccormick.cx
DIR=~/mccormick.cx/projects/PodSixNet/
REMOTE=$SRV:$DIR
TARFILE=PodSixNet-$BZRREV.tar.gz

echo "Generating and uploading HTML to mccormick.cx:"
html=`markdown README`
cp COPYING web/
cp web/base.html web/index.html
rpl -q '### content ###' "$html" web/index.html 2>/dev/null
rpl -q '### version ###' "$BZRREV" web/index.html 2>/dev/null
scp web/* $REMOTE

echo "Generating tarball and uploading to mccormick.cx:"
tar -c --exclude=.bzr --exclude=$TARFILE --exclude=web -zvf $TARFILE ../PodSixNet
scp PodSixNet-$BZRREV.tar.gz $REMOTE
ssh $SRV "cd $DIR && rm PodSixNet.tar.gz && ln -s PodSixNet-$BZRREV.tar.gz PodSixNet.tar.gz"
