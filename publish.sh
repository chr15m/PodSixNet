#!/bin/sh

echo "Generating and uploading HTML to mccormick.cx:"
html=`markdown README`
cp web/base.html web/index.html
rpl -q '### content ###' "$html" web/index.html 2>/dev/null
scp web/* mccormick.cx:~/mccormick.cx/projects/PodSixNet/
