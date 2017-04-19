#!/bin/sh

# consider only the scoring of the results from the
# [​ English_stemmer_able_to_filter_stopwords ​ , ​ BM25Scorer ​ ] configuration.

# Details on score_aggregation.py arguments:
# score_aggregation.py <algorithm: fagin|threshold> <output_filename> <ground-truth_path> <title_scores_path> <text_scores_path>

debug_msg="AGGREGATION"

echo
echo $debug_msg - start...

echo $debug_msg "mkdir ${output_path}/aggregation"

# mkdir ${output_path}/aggregation --parents
mkdir -p ${output_path}/aggregation

echo $debug_msg "aggregation using fagin. Writing in ${output_path}/aggregation/fagin.out"

python3 scripts/score_aggregation.py fagin ${output_path}/aggregation/fagin.out ${dataset_path}/${collection_name}_Ground_Truth.tsv $OUT_ENGLISHSW_BM25S/title.tsv $OUT_ENGLISHSW_BM25S/text.tsv ${title_text_weights}

echo $debug_msg "aggregation using threshold. Writing in ${output_path}/aggregation/threshold.out"

python3 scripts/score_aggregation.py threshold ${output_path}/aggregation/threshold.out ${dataset_path}/${collection_name}_Ground_Truth.tsv $OUT_ENGLISHSW_BM25S/title.tsv $OUT_ENGLISHSW_BM25S/text.tsv ${title_text_weights}

echo $debug_msg - done!
echo
