
def fagin(k, title_scorings, text_scorings, title_weight, text_weight):
	"""

	:param k: the parameter that determines the number of docs returned
	:param title_scorings: list of tuples (docId, rank, score), sorted by decreasing score
	:param text_scorings: list of tuples (docId, rank, score), sorted by decreasing score
	:return: a list of tuples (docId, rank, score), with length k, sorted by decreasing score,
	"""
	rank = {}

	title_dict = dict(map(lambda x: (x[0], x[2]), title_scorings))
	text_dict = dict(map(lambda x: (x[0], x[2]), text_scorings))

	max_num_list = max(len(title_scorings), len(text_scorings))
	correct_title_scorings = title_scorings[:]+[[None, None, None]] * (max_num_list - len(title_scorings))
	correct_text_scorings = text_scorings + ([[None, None, None]] * (max_num_list - len(text_scorings)))

	seen = compute_seen_doc_ids(k, title_scorings, text_scorings)

	for doc_id in seen:
		score = title_weight * title_dict.get(doc_id, 0) + text_weight * text_dict.get(doc_id, 0)
		rank[doc_id] = score

	sorted_rank = sorted(list(rank.items()), key=lambda x: x[1], reverse=True)[:k]
	# adding the rank 'i' for each entry:
	sorted_rank = [(entry[0], i+1, entry[1]) for i, entry in enumerate(sorted_rank)]
	return sorted_rank


def compute_seen_doc_ids(k, title_scorings, text_scorings):
	counter = 0
	seen = set()

	for title_entry, text_entry in zip(title_scorings, text_scorings):
		title_entry_id, text_entry_id = title_entry[0], text_entry[0]

		if title_entry_id in seen:
			counter += 1
		elif title_entry_id:
			seen.add(title_entry_id)

		if text_entry_id and text_entry_id in seen:
			counter += 1
		elif text_entry_id:
			seen.add(text_entry_id)

		if counter >= k:
			break

	return seen