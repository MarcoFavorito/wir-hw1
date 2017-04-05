find ../data/cran -iname \*.html | java it.unimi.di.big.mg4j.document.FileSetDocumentCollection -f HtmlDocumentFactory -p encoding=UTF-8 cran.collection

# Stemmer code
# 0: default stemmer
# 1: EnglishStemmer​
# 2: EnglishStemmer​StopWords

echo "prova $1" 
if [ "$1" -eq 0 ]; then
	echo "default stemmer used";
	java it.unimi.di.big.mg4j.tool.IndexBuilder --downcase -S cran.collection cran;
elif [  "$1" -eq 1 ]; then
	echo "english stemmer used";
	java it.unimi.di.big.mg4j.tool.IndexBuilder -t it.unimi.di.big.mg4j.index.snowball.EnglishStemmer​ --downcase -S cran.collection cran;
elif [  "$1" -eq 2 ]; then
	echo "english stemmer stop word used";
	java it.unimi.di.big.mg4j.tool.IndexBuilder -t homework.EnglishStemmerStopwords --downcase -S cran.collection cran;
else echo "ERRORE!";
fi
# ****** Scorer ******
#Default: BM25Scorer, VignaScorer

#ConstantScorer. Each document has a constant score (default is 0)
#$score ConstantScorer

# CountScorer. It is the product between the number of occurrences of the term in the document and the weight assigned to the index
#$score CountScorer

# TfIdfScorer: implements Tf/Idf
#$score TfIdfScorer
