import sys
import file_parser
import fagin
import threshold


def aggregate_scores(algorithm_name, ground_truth, title_scorings, text_scorings, title_weight, text_weight):
	"""

	:param algorithm_name: String, either 'fagin' or 'threshold
	:param ground_truth: a dict of key: queryId and value: list of docIds
	:param title_scorings: a dict of key: queryId and value: list of tuples (docId, rank, score)
	:param text_scorings: as @title_scorings
	:return: a list of tuples (queryId, docId, rank, aggregated_score)
	"""
	results = []
	cur_results = []

	# assert(len(title_scorings) == len(text_scorings))
	query_ids = text_scorings.keys()

	for qid in query_ids:
		ground_truth_k = len(ground_truth[qid])

		try:
			title_scorings_list, text_scorings_list = title_scorings[qid], text_scorings[qid]

		except KeyError:
			if qid not in title_scorings.keys():
				title_scorings_list = []
				text_scorings_list = text_scorings[qid]
			elif qid not in text_scorings.keys():
				title_scorings_list = title_scorings[qid]
				text_scorings_list = []
			else:
				raise Exception("PANIC, TURN OFF THE LAPTOP AND TAKE A COFFEE")
		finally:

			max_num_list = max(len(title_scorings_list), len(text_scorings_list))
			correct_title_scorings_list = title_scorings_list[:] + [[None, None, None]] * (max_num_list - len(title_scorings_list))
			correct_text_scorings_list = text_scorings_list[:] + ([[None, None, None]] * (max_num_list - len(text_scorings_list)))

			if algorithm_name == "fagin":
				cur_results = fagin.fagin(ground_truth_k, correct_title_scorings_list, correct_text_scorings_list, title_weight,
										  text_weight)
			elif algorithm_name == "threshold":
				cur_results = threshold.threshold(ground_truth_k, correct_title_scorings_list, correct_text_scorings_list, title_weight,
												  text_weight)

			cur_results = [ tuple([qid]+list(result))  for result in cur_results]
			results += cur_results

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
	# Check program arguments
	if len(sys.argv) < 8:
		print_usage()
		return -1

	algorithm_name, output_filename, ground_truth_filename, \
		title_scorings_filename, text_scorings_filename,\
		title_weight, text_weight = parse_args()

	ground_truth_dict = file_parser.file2dict_qid(open(ground_truth_filename, "r"), [int, int])
	title_scorings_dict = file_parser.file2dict_qid(open(title_scorings_filename, "r"), [int, int, int, float])
	text_scorings_dict = file_parser.file2dict_qid(open(text_scorings_filename, "r"), [int, int, int, float])

	results = aggregate_scores(algorithm_name, ground_truth_dict, title_scorings_dict, text_scorings_dict, title_weight, text_weight)
	write_aggregated_score(output_filename, results)

	return 0


if __name__ == "__main__":
	main()
