#!/bin/bash

debug_msg="APPLY_SCORER_FUNCTIONS"

echo
echo $debug_msg - start

if [ ! -d out/indices ]; then
    echo $debug_msg - cannot find \"out/indices\" directory...
    echo $debug_msg - exiting...
    exit 1
fi

if [ -d out/scores ]; then
    rm -r out/scores
fi
mkdir out/scores

for stemmer in ${stemmer_names[@]}; do
    mkdir out/scores/$stemmer

    for scorer_function in ${scorer_functions[@]}; do
        mkdir out/scores/$stemmer/$scorer_function

        for field in ${fields[@]}; do
            java homework.RunAllQueries_HW \
                out/indices/$stemmer/cran \
                Cranfield_DATASET/cran_all_queries.tsv \
                $scorer_function \
                $field \
                out/scores/${stemmer}/${scorer_function}/${field}.tsv
        done
    done
done

echo $debug_msg - done!
echo
