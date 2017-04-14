
def threshold(k, title_scorings, text_scorings, title_weight, text_weight):
	"""

	:param k: the parameter that determines the number of docs returned
	:param title_scorings: list of tuples (docId, rank, score), sorted by decreasing score
	:param text_scorings: list of tuples (docId, rank, score), sorted by decreasing score
	:return: a list of tuples (docId, rank, score), with length k, sorted by decreasing score,
	"""

	seen = {}
	title_dict = dict(map(lambda x: (x[0], x[2]), title_scorings))
	text_dict = dict(map(lambda x: (x[0], x[2]), text_scorings))

	for title_entry, text_entry in zip(title_scorings, text_scorings):
		title_entry_id, text_entry_id = title_entry[0], text_entry[0]
		title_entry_score, text_entry_score = title_entry[2], text_entry[2]

		if not title_entry_id:
			title_entry_score = 0
		if not text_entry_id:
			text_entry_id = 0

		cur_threshold = title_weight * title_entry_score + text_weight * text_entry_score

		if title_entry_id:
			seen[title_entry_id] = title_weight * title_dict.get(title_entry_id, 0) + text_weight * text_dict.get(title_entry_id, 0)
		if text_entry_id:
			seen[text_entry_id] = title_weight * title_dict.get(text_entry_id, 0) + text_weight * text_dict.get(text_entry_id, 0)

		top_k = sorted(list(seen.items()), key=lambda x: x[1], reverse=True)[:k]

		if len(top_k) >= k and all([score >= cur_threshold for _, score in top_k]):
			top_k = [(entry[0], i+1, entry[1]) for i, entry in enumerate(top_k)]
			return top_k

	raise Exception("")

