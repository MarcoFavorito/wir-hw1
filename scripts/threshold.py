from itertools import zip_longest

def threshold(k, title_scorings, text_scorings, title_weight, text_weight):
	"""
	Applies the Fagin's Algorithm on the inputs
	:param k: the parameter that determines the number of docs returned
	:param title_scorings: list of tuples (docId, score), sorted by decreasing score
	:param text_scorings: list of tuples (docId, score), sorted by decreasing score
	:return: a list of tuples (docId, rank, score), with length k, sorted by decreasing score,
	"""

	# a dict with key: docId seen and value: score
	seen = {}

	# get data as dict with key: docId and value: score of that docId for the query
	title_dict = dict(title_scorings)
	text_dict = dict(text_scorings)

	# even if the two list of scorings are of variable length,
	# itertools.zip_longest fills the shorter list with "None" values
	# and make the two list with equal length
	for title_entry, text_entry in zip_longest(title_scorings, text_scorings):
		# take the pair (ids, score)if the entry exists, otherwise return (None, 0)
		title_entry_id, title_entry_score = (title_entry[0], title_entry[1]) if type(title_entry) is tuple else (None, 0)
		text_entry_id, text_entry_score = (text_entry[0], text_entry[1]) if type(text_entry) is tuple else (None, 0)

		# compute the threshold of the current iteration
		cur_threshold = title_weight * title_entry_score + text_weight * text_entry_score

		# if the id is not None, add it to the "seen" and associate it with its aggregated score
		# retrieve the scores with "random access" through dictionaries
		if title_entry_id:
			seen[title_entry_id] = title_weight * title_dict.get(title_entry_id, 0) + text_weight * text_dict.get(title_entry_id, 0)
		if text_entry_id:
			seen[text_entry_id] = title_weight * title_dict.get(text_entry_id, 0) + text_weight * text_dict.get(text_entry_id, 0)

		# sort the list of (docId, score) by decreasing score and take the first k
		top_k = sorted(list(seen.items()), key=lambda x: x[1], reverse=True)[:k]

		# IF
		# 	the list of best #k element has length at least #k
		# 	AND
		# 	all the scores of these docs are greater than the current threshold
		# THEN
		# 	RETURN that list
		if len(top_k) >= k and all([score >= cur_threshold for _, score in top_k]):
			return top_k

	raise Exception("There should be at least k elements...")

