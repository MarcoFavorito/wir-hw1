import sys

# input file format
# Query ID \t DocID \t Rank \t Score

def fagin(k, ranking_dictionaries, ranking_lists):
    """Docstring"""

    seen = {}
    row = counter = 0

    # IGNORA I SEGUENI COMMENTI: ora usiamo k = numero di documenti nella ground truth...
    #
    # calcola il limite massimo di row che possono essere lette in tutti i file/ranking list considerati)
    #
    # ***************************************************************************
    #
    # serve per risolvere il caso in cui, PER UN CERTO QueryID:
    # numero di entries nel title.tsv  != numero di entries nel text.tsv
    #
    # (da vedersi per esempio, nei rispettivi file title.tsv e text.tsv,
    # tali numeri per QueryID in [10, 13, 14, 15...] )
    #
    # IL CASO PATOLOGICO era in QueryID = 15, dove rispettivamente per title e text:
    #   len(ranking_lists[0])=22     and     len(ranking_lists[1])=160
    # Evidentemente, non riusciva a trovare k=10 entries in comune nelle due liste entro 22 row,
    # ed è per questo che andava in "index out of range"
    #
    # ***************************************************************************
    #
    # potevo anche scrivere:
    # max_row_num = min(
    #   len(ranking_lists[0]),  #title.tsv
    #   len(ranking_lists[1])   #text.tsv
    # )
    # qui invece ho usato "list comprehension"
    # max_row_num = min([len(ranking_list) for ranking_list in ranking_lists])
    #
    # OSSERVAZIONE (da controllare): se la lunghezza massima dei miei file (ovvero ranking list)
    # è max_row_num, allora k non può essere più grande di max_row_num... giusto?


    # while counter < k and row < max_row_num:
    while counter < k:
        for ranking_list in ranking_lists:
            # se la ranking list corrente non ha abbastanza row
            # (mentre l'altra sì), allora salta e vai all'altra lista.
            if row >= len(ranking_list):
                continue
            doc_id, score = ranking_list[row]

            if doc_id not in seen:
                seen[doc_id] = [doc_id, score, 1]
            else:
                # Lo score si può riassegnare nel for-loop successivo, considerando facilmente
                # se stiamo sommando lo score di title o di text.
                seen[doc_id][1] += score
                seen[doc_id][2] = 2
                counter += 1
        row += 1

    for doc_id, info in seen.items():
        # commentato perché tanto vale ricalcolare tutto da capo
        # if info[2] < 2:
        #     score = 0
        score = 0
        for i, ranking_dictionary in enumerate(ranking_dictionaries):
            # if i == 0 stiamo considerando i title (quindi lo score va valutato il doppio), altrimenti il text.
            if i==0:
                score += 2*ranking_dictionary.get(doc_id, 0)
            else:
                score += ranking_dictionary.get(doc_id, 0)

        seen[doc_id][1] = score

    return sorted(list(seen.values()), key=lambda x: x[1], reverse=True)[:k]

def threshold(k, ranking_dictionaries, ranking_lists):
    """Docstring"""

    seen = {}
    title_list = ranking_lists[0]
    text_list = ranking_lists[1]
    title_dict = ranking_dictionaries[0]
    text_dict = ranking_dictionaries[1]


    for title_entry, text_entry in zip(title_list, text_list):
        title_entry_id = title_entry[0]
        text_entry_id = text_entry[0]
        title_entry_score = title_entry[1]
        text_entry_score = text_entry[1]

        cur_threshold = 2*title_entry_score + text_entry_score

        seen[title_entry_id] = 2*title_dict.get(title_entry_id, 0) + text_dict.get(title_entry_id, 0)
        seen[text_entry_id] = 2*title_dict.get(text_entry_id, 0) + text_dict.get(text_entry_id, 0)

        top_k = list(seen.items())
        top_k.sort(key=lambda x: x[1], reverse=True)
        top_k = top_k[:k]

        if all([score>=cur_threshold for _,score in top_k]) and len(top_k)>=k: return top_k
        # failed = False
        # for docId, score in top_k:
        #     if score < cur_threshold:
        #         failed = True
        #         break
        #
        # if not failed:
        #     return top_k

    raise Exception("qualcosa non va...")

def aggregate_scores(algorithm_name, query_dictionaries, query_lists, ground_truth_list):
    """Docstring"""

    results = []

    # IGNORA QUESTI COMMENTI
    #calcola il massimo k che si può utilizzare
    #max_row_num = min([len(query_list) for query_list in query_lists])

    ground_truth_k = len(ground_truth_list)


    if algorithm_name == "fagin":
        results = fagin(ground_truth_k, query_dictionaries, query_lists)

    elif algorithm_name == "threshold":
        results = threshold(ground_truth_k, query_dictionaries, query_lists)

    return results

def results_to_file(output_file, query_id, results):
    """Docstring"""
    for i in range(len(results)):
        line = str(query_id) \
            + "\t" + str(results[i][0]) \
            + "\t" + str(i+1) \
            + "\t" + str(results[i][1])

        print(line, file=output_file)

def get_line_entries(line):
    """Docstring"""

    line_entries = line.split('\t')

    query_id = int(line_entries[0])
    doc_id = int(line_entries[1])
    # rank = int(line_entries[2])
    score = float(line_entries[3])

    # return (query_id, doc_id, rank, score)
    return (query_id, doc_id, score)


def get_ground_truth(ground_truth_file):
    file = ground_truth_file.read()
    res = {}

    def add_to_dict(line, d):
        splitted_row = line.split("\t")
        qId, docId = int(splitted_row[0]), int(splitted_row[1])
        if qId not in d.keys():
            d[qId] = []
        d[qId].append(docId)

    for line in file.splitlines()[1:]:
        add_to_dict(line,res)

    return res


def __main():

    # Check program arguments
    if len(sys.argv) < 6:
        print()
        print("Usage: "
              "python score_aggregation "
              "algorithm_name "
              "output_file_name "
              "ground_truth "
              "scorings_1 scorings_2 ...")
        print()
        print("Example: "
              "python "
              "score_aggregation "
              "fagin "
              "fagin.out "
              "ground_truth.tsv "
              "title.tsv text.tsv ...")
        return

    # Algorithm name must be either "fagin" or "threshold"
    algorithm_name = sys.argv[1].lower()
    if algorithm_name != "fagin" and algorithm_name != "threshold":
        print()
        print("Error: the algorithm must be either \"fagin\" or \"threshold\"")
        print("Error: exiting...")
        print()
        return

    # File names
    output_file_name = sys.argv[2]

    input_file_names = []
    for i in range(4, len(sys.argv)):
        input_file_names.append(sys.argv[i])

    # Open output file and write the first line
    output_file = open(output_file_name, "w")
    print("QueryID\tDocID\tRank\tScore", file=output_file)

    input_files = []
    for input_file_name in input_file_names:
        input_file = open(input_file_name)
        first_line = input_file.readline()
        if first_line != "Query_ID\tDoc_ID\tRank\tScore\n":
            print()
            print("Error: wrong format for " + input_file_name + "!")
            print("Error: exiting...")
            return
        input_files.append(input_file)

    current_query = 1
    query_dictionaries = []
    query_lists = []
    current_queries = []
    eofs = []

    for input_file in input_files:
        query_dictionaries.append({})
        query_lists.append([])
        current_queries.append(1)
        eofs.append(False)

    ground_truth_filename = sys.argv[3]
    ground_truth_dictionary = get_ground_truth(open(ground_truth_filename, "r"))


    while eofs.count(False) > 1:

        for i in range(len(input_files)):
            if not eofs[i] and current_queries[i] == current_query:
                # serve per "undo" la lettura della riga della prossima query
                cur_pos = input_files[i].tell()
                input_line = input_files[i].readline()
                if not input_line:
                    eofs[i] = True
                else:
                    (current_queries[i], doc_id, score) = get_line_entries(input_line)
                    if current_queries[i] != current_query:
                        # inizio nuovo set di doc-score, ovver query successiva
                        input_files[i].seek(cur_pos)
                    else:
                        query_dictionaries[i][doc_id] = score
                        query_lists[i].append((doc_id, score))
                    assert(len(query_dictionaries[i])==len(query_lists[i]))
        if current_queries.count(current_query) == 0 or eofs.count(False) == 0:

            results = aggregate_scores(
                algorithm_name,
                query_dictionaries,
                query_lists,
                ground_truth_dictionary[current_query]
            )

            results_to_file(output_file, current_query, results)

            current_query = min(current_queries)

            query_dictionaries = []
            query_lists = []
            for input_file in input_files:
                query_dictionaries.append({})
                query_lists.append([])


__main()
