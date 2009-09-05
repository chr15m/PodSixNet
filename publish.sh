#!/bin/sh

BZRREV=`bzr log -r -1.. --line | cut -d":" -f 1`
REMOTE=mccormick.cx:~/mccormick.cx/projects/PodSixNet/
TARFILE=PodSixNet-$BZRREV.tar.gz

echo "Generating and uploading HTML to mccormick.cx:"
html=`markdown README`
cp web/base.html web/index.html
rpl -q '### content ###' "$html" web/index.html 2>/dev/null
rpl -q '### version ###' "$BZRREV" web/index.html 2>/dev/null
scp web/* $REMOTE

echo "Generating tarball and uploading to mccormick.cx:"
rm $TARFILE
tar -c --exclude=.bzr --exclude=$TARFILE --exclude=web -zvf $TARFILE ../PodSixNet
scp PodSixNet-$BZRREV.tar.gz $REMOTE

