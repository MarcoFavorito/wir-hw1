from math import log2

def maximumMDCG(k):
    res = 1 + sum([1/log2(rank+1) for rank in range(1, k)])
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
    max_MDCG = maximumMDCG(k)

    res = cur_MDCG / max_MDCG
    return res


def averaged_nMDCG(k, all_retrieved_docs, all_relevant_docs):
    nMDCG_values = []
    queryIds = all_relevant_docs.keys()
    for qid in queryIds:
        # se non ho trovato nessun documento per una certa query,
        # non ho docs per calcolare nMDCG, quindi è pari a 0
        if qid not in all_retrieved_docs.keys():
            cur_nMDCG = 0
        else:
            cur_retrieved_docs = all_retrieved_docs[qid]

            # prendo solo gli ids
            cur_retrieved_doc_ids = [entry[0] for entry in cur_retrieved_docs]
            cur_relevant_doc_ids = all_relevant_docs[qid]

            # serve per gestire il caso in cui k è maggiore del numero di retrieved docs.
            # in tal caso, k non può essere più grande di quel numero.
            cur_k = k
            max_k = len(cur_retrieved_docs)
            if cur_k>max_k:
                cur_k=max_k

            cur_nMDCG = nMDCG(cur_k, cur_retrieved_doc_ids, cur_relevant_doc_ids)
        nMDCG_values.append(cur_nMDCG)

    averaged_nMDCG = sum(nMDCG_values)/len(nMDCG_values)

    return averaged_nMDCG

