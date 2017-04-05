# Four steps:
# 1. Build Document collection
# 2. Build the Inverted Index
# 3. Query the index
# 4. Scorer

# ********************************
# ****** DocumentCollection ******
# ********************************

#First of all, build a document collection
#java it.unimi.di.big.mg4j.document.FileSetDocumentCollection --help

#find returns the list of files, one per line. This list is provided as input to the main method of the FileSetDocumentCollection
#-f specify the type of factory. -p the encoding.
find ../data/cran -iname \*.html | java it.unimi.di.big.mg4j.document.FileSetDocumentCollection -f HtmlDocumentFactory -p encoding=UTF-8 cran.collection


# ********************************
# ****** IndexBuilder ******
# ********************************

#java it.unimi.di.big.mg4j.tool.IndexBuilder --help

#--downcase: this option forces all the terms to be downcased
#-S : specifies that we are producing an index for the specified collection. If the option is omitted, Index expects to index a document sequence read from standard input :o
#dis: basename of the index

#If you have memory problem, you can use -Xmx for allocating more memory to Java.
#this will generate a lot of files
#Use the option --keep-batches to not delete temporary files
java it.unimi.di.big.mg4j.tool.IndexBuilder -t  $1 --downcase -S cran.collection cran

# ********************************
# ****** Query ******
# ********************************

#help
#java it.unimi.di.big.mg4j.query.Query --help

# Querying the index:
#java it.unimi.di.big.mg4j.query.Query -h -i FileSystemItem -c dis.collection dis-text dis-title

# Web browser: http://localhost:4242/Query•
# Command line: {text, title} > computer


# ****** Scorer ******
#Default: BM25Scorer, VignaScorer

#ConstantScorer. Each document has a constant score (default is 0)
#$score ConstantScorer

# CountScorer. It is the product between the number of occurrences of the term in the document and the weight assigned to the index
#$score CountScorer

# TfIdfScorer: implements Tf/Idf
#$score TfIdfScorer
