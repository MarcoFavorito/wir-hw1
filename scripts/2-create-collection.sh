#!/bin/sh

debug_msg="CREATE_COLLECTION"

echo
echo $debug_msg - start...

echo ${output_path}

if [ ! -d ${output_path} ]; then
    echo $debug_msg - creating \"${output_path}\" directory...
    # mkdir ${output_path} --parents
    mkdir -p ${output_path}
fi

find $collection_path -iname \*.html | \
    java it.unimi.di.big.mg4j.document.FileSetDocumentCollection \
        -f HtmlDocumentFactory -p encoding=UTF-8 $output_path/$collection_name.collection

echo $debug_msg - done!
echo
