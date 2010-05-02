#!/bin/bash

BZRREV=`bzr revno`
SRV=mccormick.cx
DIR='~/mccormick.cx/projects/PodSixNet/'
REMOTE=$SRV:$DIR
TARFILE=PodSixNet-$BZRREV.tar.gz

echo "Generating and uploading HTML to mccormick.cx:"
cp COPYING web/
html=`markdown README`
infile=`cat web/base.html`
echo "${infile//\#\#\# content \#\#\#/$html}" > web/index.html
infile=`cat web/index.html`
echo "${infile//\#\#\# version \#\#\#/$BZRREV}" > web/index.html
scp web/* $REMOTE

echo "Exporting tarball and uploading to mccormick.cx"
bzr export PodSixNet-$BZRREV.tar.gz .
scp PodSixNet-$BZRREV.tar.gz $REMOTE
ssh $SRV "cd $DIR && rm PodSixNet.tar.gz && ln -s PodSixNet-$BZRREV.tar.gz PodSixNet.tar.gz"

echo "Pushing changes to google code"
#bzr svn-push https://mccormix@podsixnet.googlecode.com/svn/podsixnet/
bzr push svn+https://mccormix@podsixnet.googlecode.com/svn/podsixnet/
