if [ $# != 2 ]
  then
    echo "No arguments supplied"
		echo "Usage: main.sh <dataset_path> <collection_name>"
		echo -e "Examples:"
		echo -e "\tmain.sh Cranfield_DATASET cran"
		echo -e "\tmain.sh Time_DATASET time"
		exit -1
fi

echo "Setting environment..."

export dataset_path=$1
export collection_name=$2
export collection_path=$dataset_path/$collection_name
export ground_truth=${collection_path}/${collection_name}_all_queries.tsv
export output_path=out/${collection_name}


export HW_DIR="$(pwd)"
export stemmers=( it.unimi.di.big.mg4j.index.NullTermProcessor it.unimi.di.big.mg4j.index.snowball.EnglishStemmer homework.EnglishStemmerStopwords )
export stemmer_names=( default english englishsw )
export scorer_functions=( CountScorer TfIdfScorer BM25Scorer )
export fields=( text title text_and_title )
export OUT_ENGLISHSW_BM25S=${output_path}/scores/englishsw/BM25Scorer

export k_values=( 1 3 5 10 )
export title_text_weights=" 2 1 "

echo "Calling the main script..."
source run.sh
