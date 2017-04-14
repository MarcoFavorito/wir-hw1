import sys
import file_parser
import fagin
import threshold


def aggregate_scores(algorithm_name, ground_truth, title_scorings, text_scorings, title_weight, text_weight):
	"""
	Aggregate scores from @title_scorings and @text_scorings
	with weights, respectively, @title_weight and @text_weight,
	using the @algorithm_name: either Fagin Algorithm or Threshold Algorithm.

	:param algorithm_name: String, either 'fagin' or 'threshold
	:param ground_truth: a dict of key: queryId and value: list of docIds
	:param title_scorings: a dict of key: queryId and value: list of tuples (docId, rank, score)
	:param text_scorings: as @title_scorings
	:return: a list of tuples (queryId, docId, rank, aggregated_score)
	"""
	results = []
	cur_results = []

	# get all the query ids from the ground truth
	query_ids = ground_truth.keys()

	# compute the aggregated rank for each query
	for qid in query_ids:
		# get the 'k' parameter for the current query
		# compute it as the number of docs in the ground truth
		ground_truth_k = len(ground_truth[qid])

		# get the list of (docs, rank, score) for each input (scoring list for title and text).
		# it may happen that some query are not retrieved for some ranking list
		# if it is the case, some of the two list will have zero elements to aggregate.
		title_scorings_list = title_scorings.get(qid, [])
		text_scorings_list = text_scorings.get(qid, [])

		# reduce the tuples of the list:
		# (docId, rank, score) => (docId, score)
		title_scorings_list = [(x[0], x[2]) for x in title_scorings_list]
		text_scorings_list = [(x[0], x[2]) for x in text_scorings_list]

		# dispach the call to the algorithm: either fagin or threshold
		cur_results = apply_aggregation_algorithm(algorithm_name, ground_truth_k, title_scorings_list, text_scorings_list, title_weight, text_weight)

		# rewrite the result in the format: (qId, docId, rank, score)
		cur_results = [tuple([qid]+[result[0], i+1, result[1]]) for i, result in enumerate(cur_results)]
		# concatenate the result of the current query to the all results computed until now
		results += cur_results

	return results

def apply_aggregation_algorithm(algorithm_name, ground_truth_k, title_scorings_list, text_scorings_list, title_weight, text_weight):
	if algorithm_name == "fagin":
		results = fagin.fagin(ground_truth_k, title_scorings_list, text_scorings_list, title_weight, text_weight)
	elif algorithm_name == "threshold":
		results = threshold.threshold(ground_truth_k, title_scorings_list, text_scorings_list, title_weight, text_weight)
	return results

def print_usage():
	print()
	print("Usage: "
		  "python score_aggregation.py "
		  "algorithm_name "
		  "output_file_name "
		  "ground_truth "
		  "title_scorings text_scorings"
		  "title_weight text_weight ")
	print()
	print("Example: "
		  "python "
		  "score_aggregation.py "
		  "fagin "
		  "fagin.out "
		  "ground_truth.tsv "
		  "title.tsv text.tsv "
		  "2 1")
	return


def parse_args():
	algorithm_name = sys.argv[1].lower()
	output_filename = sys.argv[2]
	ground_truth_filename = sys.argv[3]
	title_scorings_filename = sys.argv[4]
	text_scorings_filename = sys.argv[5]
	title_weight = float(sys.argv[6])
	text_weight = float(sys.argv[7])
	return algorithm_name, output_filename, ground_truth_filename, \
		   title_scorings_filename, text_scorings_filename, \
		   title_weight, text_weight


def validate_input(algorithm_name):
	res = True
	# Algorithm name must be either "fagin" or "threshold"
	if algorithm_name != "fagin" and algorithm_name != "threshold":
		print()
	print("Error: the algorithm must be either \"fagin\" or \"threshold\"")
	print("Error: exiting...")
	print()
	res = False

def write_aggregated_score(output_filename, results):
	with open(output_filename, "w") as out:
		print("QueryID\tDocID\tRank\tScore", file=out)
		for res in results:
			print("%d\t%d\t%d\t%.15f" % res, file=out)


def main():
	"""
	algorithm_name: fagin|threshold
	output_file_name: a path of a file where the programs will write the output
	ground_truth: a path to a ground truth
	  	(format: tab-separated values [qId:Int, docId:Int, rank:Int, score:Float]
	title_scorings: a path to a ranking list for the title field.
	  	(format: see @ground_truth)
	text_scorings: a path to a ranking list for the text field.
	  	(format: see @ground_truth)
	title_weight: how much the title score has to be weightened
	text_weight: how much the text score has to be weightened
	:return: 0 if the aggregated score has been written successfully in the output_filename
	"""
	# Check program arguments
	if len(sys.argv) < 8:
		print_usage()
		return -1

	algorithm_name, output_filename, ground_truth_filename, \
		title_scorings_filename, text_scorings_filename,\
		title_weight, text_weight = parse_args()

	# parse the input:
	# 	from list of (qid, ...)
	# 	to dict with key:qId and value: a list of the other values of the rows having the same qId
	ground_truth_dict = file_parser.file2dict_qid(open(ground_truth_filename, "r"), [int, int])
	title_scorings_dict = file_parser.file2dict_qid(open(title_scorings_filename, "r"), [int, int, int, float])
	text_scorings_dict = file_parser.file2dict_qid(open(text_scorings_filename, "r"), [int, int, int, float])

	# compute the aggregate score as a list of tuples (queryId, docId, rank, aggregated_score)
	results = aggregate_scores(algorithm_name, ground_truth_dict, title_scorings_dict, text_scorings_dict, title_weight, text_weight)

	# write the result in the output_filename
	write_aggregated_score(output_filename, results)

	return 0


if __name__ == "__main__":
	main()
