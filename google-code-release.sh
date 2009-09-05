#!/bin/sh

BZRREV=`bzr log -r -1.. --line | cut -d":" -f 1`

echo "moving trunk out the way"
svn mv https://mccormix@podsixnet.googlecode.com/svn/trunk/ https://mccormix@podsixnet.googlecode.com/svn/tags/bzr-$BZRREV/ -m 'archiving repo pre-$BZRREV'
echo "importing into google code's svn"
svn import https://mccormix@podsixnet.googlecode.com/svn/trunk/ -m 'latest version of code from the bzr repo version $BZRREV'

echo "Importing documentation"
mkdir wiki
echo '#labels Featured' > wiki/Readme.wiki
cat README | markdown | sed -e "s/<pre><code>/\{\{\{\n/" -e "s/<\/code><\/pre>/\}\}\}/" >> wiki/Readme.wiki
cd wiki
svn mv https://mccormix@podsixnet.googlecode.com/svn/wiki/ https://mccormix@podsixnet.googlecode.com/svn/tags/wiki-bzr-$BZRREV/ -m 'archiving wiki pre-$BZRREV'
svn import https://mccormix@podsixnet.googlecode.com/svn/wiki/ -m 'latest version of the wiki bzr repo version $BZRREV'
rm -rf wiki
