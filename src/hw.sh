rm -R output
mkdir output
./create_collection.sh 


stemmers=("default stemmer", "EnglishStemmer​", "EnglishStemmer​StopWords")
scorers=("CountScorer" "TfIdfScorer" "BM25Scorer")
for index in ${!stemmers[*]}; do
	current_stemmer=${stemmers[$index]}
	echo "Using stemmer ${current_stemmer}"
	./create_index.sh cran.collection "$index"
	for current_scorer in ${scorers[*]}; do
		echo "Run all queries using the scorer: ${current_scorer}"
		java homework.RunAllQueries_HW "cran" cran_all_queries.tsv "${current_scorer}" "text_and_title" "output/output_cran__${current_stemmer}__${current_scorer}.tsv"
	done
	rm cran-*
done
