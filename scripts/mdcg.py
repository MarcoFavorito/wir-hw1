from math import log2

def maximumMDCG(k, groundTruth):

    # if k is greater equal the number of relevant docs
    # (i.e. the length of @groundTruth) then
    # Compute MDCG with the number of relevant docs.
    max_k = k if k < len(groundTruth) else len(groundTruth)
    
    res = 1 + sum([1/log2(rank+1) for rank in range(1, max_k)])
    return res

def relevance(docId, groundTruth):
    return 1 if docId in groundTruth else 0

def MDCG(k, retrieved_docs, groundTruth):
    res = 0
    res += relevance(retrieved_docs[0], groundTruth)
    for i in range(1, k):
        res += relevance(retrieved_docs[i], groundTruth)/log2(i+1)

    return res


def nMDCG(k, retrieved_docs, groundTruth):
    cur_MDCG = MDCG(k, retrieved_docs, groundTruth)
    max_MDCG = maximumMDCG(k, groundTruth)

    res = cur_MDCG / max_MDCG
    return res


def averaged_nMDCG(k, all_retrieved_docs, all_relevant_docs):
    """
    :param all_retrieved_docs:  dict[key: qId, value: list[(docId, rank, score)] sorted by score ]
    :param all_relevant_docs:   dict[key: qId, value: list[(docId)]
    :return: averaged nMDCG on every queries
    """
    nMDCG_values = []
    queryIds = all_relevant_docs.keys()
    for qid in queryIds:
        # if there is no doc for a certain query
        # we cannot compute nMDCG, so set it to 0
        if qid not in all_retrieved_docs.keys():
            cur_nMDCG = 0
        else:
            cur_retrieved_docs = all_retrieved_docs[qid]

            # take only the docIds
            cur_retrieved_doc_ids = [entry[0] for entry in cur_retrieved_docs]
            cur_relevant_doc_ids = all_relevant_docs[qid]

            # handle the case when k is greater than the number of retrieved docs
            # in that case, k cannot be greater than that number
            cur_k = k
            max_k = len(cur_retrieved_docs)
            if cur_k>max_k:
                cur_k=max_k

            # compute nMDCG for the current query
            cur_nMDCG = nMDCG(cur_k, cur_retrieved_doc_ids, cur_relevant_doc_ids)
        nMDCG_values.append(cur_nMDCG)

    averaged_nMDCG = sum(nMDCG_values)/len(nMDCG_values)

    return averaged_nMDCG