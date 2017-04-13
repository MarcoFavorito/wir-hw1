#!/bin/sh

# Details on evaluation.py arguments:
# evaluation.py <metric: precision|mdcg> <output_filename> <ground-truth_path> <ranking-list>

debug_msg="MAKE_PLOTS"

echo
echo $debug_msg - start

if [ ! -d out/evaluation/plots ]; then
    echo $debug_msg - cannot find \"out/evaluation/plots\" directory...
    echo $debug_msg - exiting...
    exit 1
fi

for stemmer in ${stemmer_names[@]}; do

    for scorer_function in ${scorer_functions[@]}; do
				OPTIONS=""
        for field in ${fields[@]}; do
						OPTIONS="${OPTIONS} $field out/evaluation/plots/averaged_nMDCG_${stemmer}_${scorer_function}_${field}.out"
				done

				python scripts/make_plots.py out/evaluation/plots/${stemmer}_${scorer_function}.plot "Averaged nMDCG for ${stemmer}_${scorer_function}" $OPTIONS
		done
done

echo $debug_msg - done!
echo
