rm -R output
mkdir output
./create_collection.sh 


stemmers=("default_stemmer" "EnglishStemmer​" "EnglishStemmer​StopWords")
scorers=("CountScorer" "TfIdfScorer" "BM25Scorer")
modes=("text_and_title" "text" "title")
for index in ${!stemmers[*]}; do
	current_stemmer=${stemmers[$index]}
	echo "Using stemmer ${current_stemmer}"
	./create_index.sh cran.collection "$index"
	for current_scorer in ${scorers[*]}; do
		echo "Run all queries using the scorer: ${current_scorer}"
		for current_mode in ${modes[*]}; do
			echo "Using mode ${current_mode}"
			java homework.RunAllQueries_HW "cran" cran_all_queries.tsv "${current_scorer}" "${current_mode}" "output/output_cran__${current_stemmer}__${current_scorer}__${current_mode}.tsv"
		done
	done
	rm cran-*
done
