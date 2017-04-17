#!/bin/sh

debug_msg="BUILD_INDEX"

build_index () {
    stemmer=$1
    stemmer_name=$2

    echo $debug_msg - creating new \"${output_path}/indices/$stemmer_name\" folder...
    mkdir ${output_path}/indices/$stemmer_name --parents

    java it.unimi.di.big.mg4j.tool.IndexBuilder -t $stemmer -S ${output_path}/$collection_name.collection ${output_path}/indices/$stemmer_name/$collection_name

		# create a link for the .collection file into the index folder.
    ln ${output_path}/$collection_name.collection ${output_path}/indices/$stemmer_name/$collection_name.collection
}

echo
echo $debug_msg - start...

if [ ! -d out ]; then
    echo $debug_msg - cannot find \"out\" directory...
    echo $debug_msg - exiting...
    exit 1
fi

if [ -d ${output_path}/indices ]; then
    rm -r ${output_path}/indices
fi
mkdir ${output_path}/indices --parents

for i in {0..2}; do
    build_index ${stemmers[i]} ${stemmer_names[i]}
done

echo $debug_msg - done!
echo
