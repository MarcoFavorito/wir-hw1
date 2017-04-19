#!/bin/sh

debug_msg="APPLY_SCORER_FUNCTIONS"

echo
echo $debug_msg - start

if [ ! -d ${output_path}/indices ]; then
    echo $debug_msg - cannot find \"${output_path}/indices\" directory...
    echo $debug_msg - exiting...
    exit 1
fi

if [ -d ${output_path}/scores ]; then
    rm -r ${output_path}/scores
fi

for stemmer in ${stemmer_names[@]}; do
    for scorer_function in ${scorer_functions[@]}; do
        # mkdir ${output_path}/scores/$stemmer/$scorer_function --parents
        mkdir -p ${output_path}/scores/$stemmer/$scorer_function

        for field in ${fields[@]}; do
						echo "${output_path}/indices/${stemmer}/${collection_name}"
            java homework.RunAllQueries_HW \
                ${output_path}/indices/${stemmer}/${collection_name} \
                ${dataset_path}/${collection_name}_all_queries.tsv \
                $scorer_function \
                $field \
                ${output_path}/scores/${stemmer}/${scorer_function}/${field}.tsv
        done
    done
done

echo $debug_msg - done!
echo
