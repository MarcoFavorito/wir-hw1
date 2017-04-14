### Script descriptions
- `main.sh` is the entry point of our software.
>	1. Define the environment in which the application will run;
>	2. Call the script `run.sh`;

you can call it in the following way:  
> `main.sh <dataset_path> <collection_name> <title_weight> <text_weight>`

examples:  
> `main.sh Cranfield_DATASET cran 2 1` 
> `main.sh Time_DATASET time 0 1`

Notice: the DATASET folder has to bestructured  (bash syntax for the variables resolution):
```
${dataset_directory}/
	${collection_name}/
	${collection_name}_Ground_Truth.tsv
	${collection_name}_all_queries.tsv
```
All the outputs are created in the folder `${outputfolder}`, i.e. `out/${collection_name}`.

- `run.sh`
> - calls all the other scripts numbered from `0-*` to `7-*`, which are described in the following;
> - **Notice**: 
- `0-clean.sh`
>	- remove the folder `out/${collection_name}`
- `1-set-my-classpath.sh`
>	- is used to set the `CLASSPATH` to `${HW_DIR}/libs`, where all `.jar` files of MG4J and the utilities provided by the tutor are located.
- `2-create-collection.sh`
>	- create the file `${collection_name}.collection` in the output folder;
- `3-build-index.sh`
>	- create an index for each possible stemmer available in the variable `stemmer_names` (in our configurations: `NullTermProcessor`, `EnglishStemmer` and `homework.EnglishStemmerStopwords`);  
>	- It stores the results in `${output_folder}/indices/${stemmer}`;  
- `4-apply-scorer-functions.sh` 
> - calls the utility `homework.RunAllQueries_HW`, which computes the score for each possible configuration, varying on Stemmer, Scorer and Fields (defined respectively in `$stemmer_names`, `$scorer_functions`, `$fields`);
> - It stores the results in `$output_folder/$stemmer/$scorer/`;
- `5-aggregation.sh`
> - computes the ranking aggregation of the configuration `EnglishStemmerStopWords` and `BM25Scorer`, both with Fagin's Algorithm and Threshold Algorithm (respectively defined in `fagin.py` and `threshold.py`, calling the script `score_aggregation.py`;
> - It stores the results in the folder `$output_folder/aggregation/${algorithm_name}.out`
> - The script is called in the following way:  
```
python score_aggregation.py algorithm_name output_file_name ground_truth title_scorings text_scorings title_weight text_weight
Where:
	- algorithm_name: either "fagin" or "threshold";
	- output_file: the path of the output file;
	- ground_truth: the path of the Ground Truth (tsv format);
	- title_scorings: the path of the scorings for the field 'title' (tsv format);
	- text_scorings: the path of the scorings for the field 'text' (tsv format);
	- title_weight: the weight to give to the title score during the aggregation;
	- text_weight: the weight to give to the text score during the aggregation;

Example:
python score_aggregation.py fagin fagin.out ground_truth.tsv title.tsv text.tsv 2 1
```
- `6-evaluation.sh`
> - produces evaluation for the various configuration, both with Averaged R-Precision and nMDCG (implemented in `r_precision.py` and `mdcg.py` modules), calling the main script `evaluation.py` five times for each stemmer-scorer-field combination: 
>		- one for the Averaged R-Precision;
>		- four for all the possible variants of nMDCG, varying on four values of the parameter $k$ defined in our default configurations: $1, 3, 5, 10$.
 > - it stores the results in the main folder `${output_folder}/evaluation/`, with the following subfolders:
 >		- `benchmark`: a set of files, one for each considered evaluation function (in our default configurations they are 5, as explained above); in each file there is an overview of all the scores for each stemmer-scorer-field combination;
 > 		- `aggregation`: a set of files, one for each considered evaluation function. In each file there is the scores for both the `fagin` and the `threshold` algorithm.
 >		- `plots`: a set of files `.out` in tsv format, one for each stemmer-scorer-filed configuration (in our default settings: 3x3x3=27 different files). In each file there is a summarization of all scores, for a certain stemmer-scorer-field configuration, obtained by every possible evaluation function (only for `Averaged nMDCG`.
 > - The script is called in the following way:  
```
python evaluation.py metric ground_truth scores [k]
Where:
	- metric: either "precision" or "mdcg", abbreviations for, respectively, "Averaged R-Precision" and "Averaged nMDCG";
	- ground_truth: the path of the Ground Truth (tsv format);
	- scores: the file .tsv of the scoring to be evaluated;
	- k: optional (only for metric=mdcg) 
Example:
python evaluation.py mdcg ground_truth.tsv scorings.tsv k

Notice: the python script only print one the stdout the computed value.	
```

- `7-make-plots.sh`
> - produces a set of plots in `svg` format, one for each stemmer-scorer configuration (3x3=9).
> - Plots are stored in `${output_dir}/evaluation/plots` directory.
>- Usage:
```
python make_plot.py out_filename plot_title <label1> <scores_filename1> <label2> <scores_filename2> ...
Where:
	- out_filename: is the path for the output plot;
	- plot_title: the title tha will be given to the plot
	- (labelX score_filenameX) pair: the label stands for the string with which the plotted function will be named in the legend; the score_filenameX contains the relative data.
```

