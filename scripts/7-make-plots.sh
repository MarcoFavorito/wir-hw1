#!/bin/sh

# Details on evaluation.py arguments:
# evaluation.py <metric: precision|mdcg> <output_filename> <ground-truth_path> <ranking-list>

debug_msg="MAKE_PLOTS"

echo
echo $debug_msg - start

if [ ! -d ${output_path}/evaluation/plots ]; then
    echo $debug_msg - cannot find \"${output_path}/evaluation/plots\" directory...
    echo $debug_msg - exiting...
    exit 1
fi

for stemmer in ${stemmer_names[@]}; do

    for scorer_function in ${scorer_functions[@]}; do
				OPTIONS=""
        for field in ${fields[@]}; do
						OPTIONS="${OPTIONS} $field ${output_path}/evaluation/plots/averaged_nMDCG_${stemmer}_${scorer_function}_${field}.out"
				done

				python scripts/make_plots.py ${output_path}/evaluation/plots/${stemmer}_${scorer_function}.plot "Averaged nMDCG for ${stemmer}_${scorer_function}" $OPTIONS
		done
done

echo $debug_msg - done!
echo
