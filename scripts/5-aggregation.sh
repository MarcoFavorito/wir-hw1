# consider only the scoring of the results from the
# [​ English_stemmer_able_to_filter_stopwords ​ , ​ BM25Scorer ​ ] configuration.

debug_msg="AGGREGATION"

echo
echo $debug_msg - start...

echo $debug_msg "mkdir $HW_DIR/out/aggregation"

mkdir $HW_DIR/out/aggregation
export OUT_ENGLISHSW_BM25S=$HW_DIR/out/scores/english_sw/BM25Scorer/

echo $debug_msg "aggregation using fagin. Writing in /out/aggregation/fagin.out"

python3 scripts/score_aggregation.py fagin out/aggregation/fagin.out Cranfield_DATASET/cran_Ground_Truth.tsv $OUT_ENGLISHSW_BM25S/title.tsv $OUT_ENGLISHSW_BM25S/text.tsv

echo $debug_msg "aggregation using threshold. Writing in /out/aggregation/threshold.out"

python3 scripts/score_aggregation.py threshold out/aggregation/threshold.out Cranfield_DATASET/cran_Ground_Truth.tsv $OUT_ENGLISHSW_BM25S/title.tsv $OUT_ENGLISHSW_BM25S/text.tsv

echo $debug_msg - done!
echo
