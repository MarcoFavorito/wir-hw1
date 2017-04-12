debug_msg="EVALUATION"

echo
echo $debug_msg - start

if [ ! -d out/indices ]; then
    echo $debug_msg - cannot find \"out/indices\" directory...
    echo $debug_msg - exiting...
    exit 1
fi

if [ -d out/evaluation ]; then
    rm -r out/evaluation
fi
mkdir out/evaluation

# Evaluation of all the possible configurations
for stemmer in ${stemmer_names[@]}; do
    mkdir out/evaluation/$stemmer

    for scorer_function in ${scorer_functions[@]}; do
        mkdir out/evaluation/$stemmer/$scorer_function

        for field in ${fields[@]}; do

						echo "Evaluating Averaged R-Precision of $stemmer/$scorer_function/${field}"
            python3 scripts/evaluation.py \
								precision \
								out/evaluation/$stemmer/$scorer_function/${field}_precision.out\
                Cranfield_DATASET/cran_Ground_Truth.tsv \
              	out/scores/${stemmer}/${scorer_function}/${field}.tsv

						echo "Evaluating nMDCG of $stemmer/$scorer_function/${field}"
						python3 scripts/evaluation.py \
								mdcg \
								out/evaluation/$stemmer/$scorer_function/${field}_mdcg.out \
								Cranfield_DATASET/cran_Ground_Truth.tsv \
								out/scores/${stemmer}/${scorer_function}/${field}.tsv
        done
    done
done

# evaluation of aggregtion algorithm results. Only Averaged R-Precision
mkdir out/evaluation/aggregation

echo "Evaluating Averaged R-Precision of 'fagin' output"
python3 scripts/evaluation.py \
		precision \
		out/evaluation/aggregation/precision.out\
		Cranfield_DATASET/cran_Ground_Truth.tsv \
		out/aggregation/fagin.out

#threshold
echo "Evaluating Averaged R-Precision of 'threshold' output"
python3 scripts/evaluation.py \
		precision \
		out/evaluation/aggregation/precision.out\
		Cranfield_DATASET/cran_Ground_Truth.tsv \
		out/aggregation/threshold.out
echo $debug_msg - done!
echo
