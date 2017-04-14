from itertools import zip_longest

def fagin(k, title_scorings, text_scorings, title_weight, text_weight):
	"""
	Applies the Fagin's Algorithm on the inputs
	:param k: the parameter that determines the number of docs returned
	:param title_scorings: list of tuples (docId, score), sorted by decreasing score
	:param text_scorings: list of tuples (docId, score), sorted by decreasing score
	:return: a list of tuples (docId, score), with length k, sorted by decreasing score,
	Notice: the lists @title_scorings and @text_scorings can be of different length (either empty!)
	"""
	rank = {}

	# get data as dict with key: docId and value: score of that docId for the query
	title_dict = dict(title_scorings)
	text_dict = dict(text_scorings)

	# computes the seen docs, according to the Fagin Algorithm
	seen = compute_seen_doc_ids(k, title_scorings, text_scorings)

	# compute the score of the seen docs, applying the correct weight
	# retrieve the scores with "random access" through dictionaries
	for doc_id in seen:
		score = title_weight * title_dict.get(doc_id, 0) + text_weight * text_dict.get(doc_id, 0)
		rank[doc_id] = score

	# sort the list of (docId, score) by decreasing score and take the first k
	sorted_rank = sorted(list(rank.items()), key=lambda x: x[1], reverse=True)[:k]

	return sorted_rank
	# get data as dict with key: docId and value: score of that docId for the query



def compute_seen_doc_ids(k, title_scorings, text_scorings):
	# the counter that keeps track of the
	# number of docId seen in both the lists
	# until a given iteration
	counter = 0
	# the set of seen docIds
	seen = set()

	# even if the two list of scorings are of variable length,
	# itertools.zip_longest fills the shorter list with "None" values
	# and make the two list with equal length
	for title_entry, text_entry in zip_longest(title_scorings, text_scorings):
		# take the ids if the entry exists, otherwise return None
		title_entry_id = title_entry[0] if type(title_entry) is tuple else None
		text_entry_id = text_entry[0] if type(text_entry) is tuple else None

		# if the id is already in the "seen" set, then increase the counter.
		# otherwise add the current docId in the set.
		if title_entry_id in seen: counter += 1
		elif title_entry_id: seen.add(title_entry_id)

		if text_entry_id in seen: counter += 1
		elif text_entry_id: seen.add(text_entry_id)

		# if we have seen for two times at least k elements,
		# then stop and return the "seen" set.
		if counter >= k:
			break

	return seen
