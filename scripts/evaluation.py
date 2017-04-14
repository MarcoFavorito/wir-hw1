import sys
import file_parser
import r_precision
import mdcg

def parse_args():
	metric = sys.argv[1].lower()
	ground_truth_filename = sys.argv[2]
	scorings_filename = sys.argv[3]
	if len(sys.argv) == 5:
		k = int(sys.argv[4])
	else:
		k=-1
	return metric, ground_truth_filename, scorings_filename, k

def print_usage():
	print()
	print("Usage: "
		  "python evaulation "
		  "metric "
		  "ground_truth "
		  "scores "
		  "[k]")
	print()
	print("Examples: "
		  "python "
		  "evaluation "
		  "precision "
		  "ground_truth.tsv "
		  "scorings.tsv "
		  "\n"
		  "python "
		  "evaluation "
		  "mdcg "
		  "ground_truth.tsv "
		  "scorings.tsv "
		  "k ")
	return -1

def input_checking(metric, k):
	available_metrics = ["precision", "mdcg"]
	try:
		assert (metric in available_metrics)
	except AssertionError as ae:
		print(metric + " has to be in: " + available_metrics)
		raise Exception

	try:
		if metric=="mdcg":
			assert(k > 0)
	except AssertionError as ae:
		print("k must be greater than 0")
		raise Exception


def main():
	"""
	metric: 'precision' for the Averaged R-Precision; 'mdcg' for Averaged nMDCG
	ground_truth: a path to a ground truth
		(format: tab-separated values [qId:Int, docId:Int, rank:Int, score:Float]
	scorings: a path to the scoring list to be evaluated
		(format: as @ground_truth)
	k (only if metric=mdcg)
	:return: 0 if the result of the evaluation has been written on the stdout
	"""
	# Check program arguments
	if len(sys.argv) < 4 or len(sys.argv) > 5:
		print_usage()
		return

	metric, ground_truth_filename, scorings_filename, k = parse_args()
	result = 0

	try:
		input_checking(metric, k)
	except Exception as e:
		return -1

	# parse the input:
	# 	from list of (qid, ...)
	# 	to dict with key:qId and value: a list of the other values of the rows having the same qId
	ground_truth_dict = file_parser.file2dict_qid(open(ground_truth_filename, "r"), [int, int])
	scorings_dict = file_parser.file2dict_qid(open(scorings_filename, "r"), [int, int, int, float])

	if metric=="precision":
		result = r_precision.averaged_R_Precision(scorings_dict, ground_truth_dict)
	elif metric=="mdcg":
		result = mdcg.averaged_nMDCG(k, scorings_dict, ground_truth_dict)
	else:
		pass

	# print to stdout the computed evaluation
	print(result)
	return 0


if __name__ == "__main__":
	main()