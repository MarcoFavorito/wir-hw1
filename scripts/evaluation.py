import sys
import file_parser

def R_precision(retrieved_docs,relevant_docs):
	"""

	:param retrieved_docs: list of tuples (docId, rank, score), sorted by score
	:param relevant_docs: list of tuples (docId) of the ground-truth
	:return:
	"""

	relevant_docs_number = len(relevant_docs)
	top_k_retrieved_docs = retrieved_docs[:relevant_docs_number]

	true_positives = 0
	false_positives = 0

	for docId, _, _ in top_k_retrieved_docs:
		if docId in relevant_docs:
				true_positives += 1
		else:
			false_positives += 1

	return true_positives / (true_positives + false_positives)

def averaged_R_Precision(all_retrieved_docs, all_relevant_docs):
	"""

	:param all_retrieved_docs:  dict[key: qId, value: list[(docId, rank, score)] sorted by score ]
	:param all_relevant_docs:   dict[key: qId, value: list[(docId)]
	:return: averaged R-Precision among all queries
	"""

	n_queries = len(all_retrieved_docs)
	precisions = []

	for qId in all_retrieved_docs.keys():
		cur_retrieved = all_retrieved_docs[qId]
		cur_relevant = all_relevant_docs[qId]
		cur_R_precision = R_precision(cur_retrieved, cur_relevant)
		precisions.append(cur_R_precision)

	average = sum(precisions)/n_queries

	return average


def print_usage():
	print()
	print("Usage: "
		  "python evaulation "
		  "metric "
		  "output_filename "
		  "ground_truth "
		  "scores ")
	print()
	print("Example: "
		  "python "
		  "evaluation "
		  "precision "
		  "r_precision.out "
		  "ground_truth.tsv "
		  "scorings.tsv")
	return

def input_checking(metric):
	available_metrics = ["precision", "mdcg"]
	try:
		assert (metric in available_metrics)
	except AssertionError:
		print(metric + " has to be in: " + available_metrics)
		raise Exception

def main():
	# Check program arguments
	if len(sys.argv) != 5:
		print_usage()
		return

	result = 0

	metric = sys.argv[1].lower()
	output_filename = sys.argv[2]
	ground_truth_filename = sys.argv[3]
	scorings_filename = sys.argv[4]

	try:
		input_checking(metric)
	except Exception:
		return -1

	ground_truth_dict = file_parser.file2dict_qid(open(ground_truth_filename, "r"), [int, int])
	scorings_dict = file_parser.file2dict_qid(open(scorings_filename, "r"), [int, int, int, float])

	assert(len(ground_truth_dict) == len(scorings_dict))

	if metric=="precision":
		result = averaged_R_Precision(scorings_dict, ground_truth_dict)
		with open(output_filename, "w") as out:
			print(result, file=out)
	elif metric=="mdcg":
		print("mdcg Not yet implemented")
		return -1
	else:
		pass

	return 0


if __name__ == "__main__":
	main()
