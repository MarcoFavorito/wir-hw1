from math import log2

def maximumMDCG(k):
    res = 1 + sum([1/log2(rank) for rank in range(2,k+1)])
    return res

def relevance(docId, groundTruth):
    return 1 if docId in groundTruth else 0

def MDCG(k, retrieved_docs, groundTruth):
    res = 0
    res += relevance(retrieved_docs[0][0], groundTruth)
    for i in range(2, k+1):
        res += relevance(retrieved_docs[i][0], groundTruth)/log2(i)

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
        cur_retrieved_docs = all_retrieved_docs[qid]
        cur_relevant_docs = all_relevant_docs[qid]
        cur_nMDCG = nMDCG(k, cur_retrieved_docs, cur_relevant_docs)
        nMDCG_values.append(cur_nMDCG)

    averaged_nMDCG = sum(nMDCG_values)/len(nMDCG_values)

    return averaged_nMDCG

