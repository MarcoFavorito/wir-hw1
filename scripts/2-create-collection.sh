#!/bin/sh

debug_msg="CREATE_COLLECTION"

echo
echo $debug_msg - start...

if [ ! -d out ]; then
    echo $debug_msg - creating \"out\" directory...
    mkdir out
fi

find Cranfield_DATASET/cran -iname \*.html | \
    java it.unimi.di.big.mg4j.document.FileSetDocumentCollection \
        -f HtmlDocumentFactory -p encoding=UTF-8 out/cran.collection

echo $debug_msg - done!
echo
