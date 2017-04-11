import sys
# file name format
# output_cran__${current_stemmer}__${current_scorer}__${current_mode}.tsv

# file format
# Query ID \t DocID \t Rank \t Score

def fagin(k, title_query_dictionary, title_query_list, text_query_dictionary, text_query_list):
    """Docstring"""

    # seen = {}

    # for (title_doc_id, title_score), (text_doc_id, text_score) in zip(title_query_list, text_query_list):
    #     if title_doc_id not in seen:
    #         seen[title_doc_id] = [title_doc_id, title_score, 1]
    #     else:
    #         seen[title_doc_id][1] += title_score
    #         seen[title_doc_id][2] = 2
    #         k -= 1

    #     if text_doc_id not in seen:
    #         seen[text_doc_id] = [text_doc_id, text_score, 1]
    #     else:
    #         seen[text_doc_id][1] += text_score
    #         seen[text_doc_id][2] = 2
    #         k -= 1

    #     if k == 0:
    #         break

    # for doc_id, info in seen.items():
    #     if info[2] < 2:
    #         seen[doc_id][1] = title_query_dictionary.get(doc_id, 0) + text_query_dictionary.get(doc_id, 0)
    #         seen[doc_id][2] = 2

    # return sorted(list(seen.values()), key=lambda x: x[1], reverse=True)[:10]

    return fagin_2(k, [title_query_dictionary, text_query_dictionary], [title_query_list, text_query_list])

def fagin_2(k, ranking_dictionaries, ranking_lists):
    """Docstring"""

    seen = {}
    row = counter = 0

    while counter < k:
        for ranking_list in ranking_lists:
            doc_id, score = ranking_list[row]

            if doc_id not in seen:
                seen[doc_id] = [doc_id, score, 1]
            else:
                seen[doc_id][1] += score
                seen[doc_id][2] = 2
                counter += 1
        row += 1

    for doc_id, info in seen.items():
        if info[2] < 2:
            score = 0
            for ranking_dictionary in ranking_dictionaries:
                score += ranking_dictionary.get(doc_id, 0)

            seen[doc_id][1] = score

    return sorted(list(seen.values()), key=lambda x: x[1], reverse=True)[:k]

def threshold(k, title_query_dictionary, title_query_list, text_query_dictionary, text_query_list):
    """Docstring"""
    return []

def threshold_2(k, ranking_dictionaries, ranking_lists):
    """Docstring"""
    return []

def get_line_entries(line):
    """Docstring"""

    line_entries = line.split('\t')

    query_id = int(line_entries[0])
    doc_id = int(line_entries[1])
    # rank = int(line_entries[2])
    score = float(line_entries[3])

    # return (query_id, doc_id, rank, score)
    return (query_id, doc_id, score)

def aggregate_scores(
        algorithm_name,
        title_query_dictionary,
        title_query_list,
        text_query_dictionary,
        text_query_list
    ):

    """Docstring"""

    results = []

    if algorithm_name == "fagin":
        results = fagin(
            10,
            title_query_dictionary,
            title_query_list,
            text_query_dictionary,
            text_query_list
        )

    elif algorithm_name == "threshold":
        results = threshold(
            10,
            title_query_dictionary,
            title_query_list,
            text_query_dictionary,
            text_query_list
        )

    return results

def aggregate_scores_2(
        algorithm_name,
        query_dictionaries,
        query_lists
    ):

    """Docstring"""

    results = []

    if algorithm_name == "fagin":
        results = fagin_2(
            10,
            query_dictionaries,
            query_lists
        )

    elif algorithm_name == "threshold":
        results = threshold_2(
            10,
            query_dictionaries,
            query_lists
        )

    return results

def results_to_file(output_file, query_id, results):
    """Docstring"""
    for i in range(len(results)):
        line = str(query_id) \
            + "\t" + str(results[i][0]) \
            + "\t" + str(i+1) \
            + "\t" + str(results[i][1])

        print(line, file=output_file)


def __main():

    # Check program arguments
    if len(sys.argv) < 5:
        print()
        print("Usage: \
            python score_aggregation \
            algorithm_name \
            output_file_name \
            file_name_1 file_name_2 ...")
        print()
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
    # title_file_name = sys.argv[3]
    # text_file_name = sys.argv[4]

    input_file_names = []
    for i in range(3, len(sys.argv)):
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

    # # Open the first file and check the first line
    # title_file = open(title_file_name)
    # first_line = title_file.readline()
    # if first_line != "Query_ID\tDoc_ID\tRank\tScore\n":
    #     print()
    #     print("Error: wrong format for " + title_file_name + "!")
    #     print("Error: exiting...")

    # # Open the second file and check the first line
    # text_file = open(text_file_name)
    # first_line = text_file.readline()
    # if first_line != "Query_ID\tDoc_ID\tRank\tScore\n":
    #     print()
    #     print("Error: wrong format for " + text_file_name + "!")
    #     print("Error: exiting...")
    #     print()

    current_query = 1
    # title_query_dictionary = {}
    # title_query_list = []
    # text_query_dictionary = {}
    # text_query_list = []

    # current_title_query = 1
    # current_text_query = 1
    # eof_text = False
    # eof_title = False

    query_dictionaries = []
    query_lists = []
    current_queries = []
    eofs = []

    for input_file in input_files:
        query_dictionaries.append({})
        query_lists.append([])
        current_queries.append(1)
        eofs.append(False)


    # while not (eof_title and eof_text):
    while eofs.count(False) > 1:

        for i in range(len(input_files)):
            if not eofs[i] and current_queries[i] == current_query:
                input_line = input_files[i].readline()
                if not input_line:
                    eofs[i] = True
                else:
                    (current_queries[i], doc_id, score) = get_line_entries(input_line)
                    query_dictionaries[i][doc_id] = score
                    query_lists[i].append((doc_id, score))

        # if not eof_title and current_title_query == current_query:
        #     title_line = title_file.readline()
        #     if not title_line:
        #         eof_title = True
        #     else:
        #         (current_title_query, title_doc_id, title_score) = get_line_entries(title_line)
        #         title_query_dictionary[title_doc_id] = title_score
        #         title_query_list.append((title_doc_id, title_score))

        # if not eof_text and current_text_query == current_query:
        #     text_line = text_file.readline()
        #     if not text_line:
        #         eof_text = True
        #     else:
        #         (current_text_query, text_doc_id, text_score) = get_line_entries(text_line)
        #         text_query_dictionary[text_doc_id] = text_score
        #         text_query_list.append((text_doc_id, text_score))

        # if current_query != current_title_query and current_query != current_text_query:
        if current_queries.count(current_query) == 0 or eofs.count(False) == 0:

            results = aggregate_scores_2(
                algorithm_name,
                query_dictionaries,
                query_lists
            )

            results_to_file(output_file, current_query, results)

            current_query = min(current_queries)

            query_dictionaries = []
            query_lists = []
            for input_file in input_files:
                query_dictionaries.append({})
                query_lists.append([])

            # results = aggregate_scores(
            #     algorithm_name,
            #     title_query_dictionary,
            #     title_query_list,
            #     text_query_dictionary,
            #     text_query_list
            # )

            # results_to_file(output_file, current_query, results)

            # current_query = current_title_query
            # title_query_dictionary = {}
            # title_query_list = []
            # text_query_dictionary = {}
            # text_query_list = []





__main()
