
def R_precision(retrieved_docs,relevant_docs):
	"""

	:param retrieved_docs: list of tuples (docId, rank, score), sorted by score
	:param relevant_docs: list of tuples (docId) of the ground-truth
	:return:
	"""

	relevant_docs_number = len(relevant_docs)

	# take only the best |ground truth| docs, according to the R-Precision
	top_k_retrieved_docs = retrieved_docs[:relevant_docs_number]

	true_positives = 0
	false_positives = 0

	# count the true positives and the true negatives
	for docId in top_k_retrieved_docs:
		if docId in relevant_docs:
			true_positives += 1
		else:
			false_positives += 1

	return true_positives / (true_positives + false_positives)

def averaged_R_Precision(all_retrieved_docs, all_relevant_docs):
	"""
	Compute the averaged R-Precision
	:param all_retrieved_docs:  dict[key: qId, value: list[(docId, rank, score)] sorted by score ]
	:param all_relevant_docs:   dict[key: qId, value: list[(docId)]
	:return: averaged R-Precision among all queries
	"""

	n_queries = len(all_relevant_docs)
	precisions = []

	# compute the R-Precision for each query and store in a list
	for qId in all_relevant_docs.keys():
		cur_retrieved = all_retrieved_docs.get(qId,[(None,None,None)])
		cur_retrieved, _, _ = zip(*cur_retrieved)
		cur_relevant = all_relevant_docs[qId]
		cur_R_precision = R_precision(cur_retrieved, cur_relevant)
		precisions.append(cur_R_precision)

	# compute the averaged R-Precision from the R-Precision of each query
	average = sum(precisions)/n_queries

	return average

