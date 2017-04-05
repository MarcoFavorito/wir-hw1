import sys
# file name format
# output_cran__${current_stemmer}__${current_scorer}__${current_mode}.tsv

# file format
# Query ID \t DocID \t Rank \t Score

def readFileLines(file_name):
    return open(file_name, "r").read().splitlines()
    
def getNextQuery():
    # TODO
    return

def fagin():
    # TODO
    return
    
def threshold():
    # TODO
    return

def main():
    # TODO

    title_file_name = sys.argv[1]
    text_file_name = sys.argv[2]
    
    title_file_lines = readFileLines(title_file_name)
    text_file_lines = readFileLines(text_file_name)
    
    d1 = {}
    d2 = {}
    for row_1, row_2 in zip(title_file_lines, text_file_lines)[1:]:
        
        l_row_1 = parse_line(row_1)
        l_row_2 = parse_line(row_2)
        qid1 = int(l_row_1[0])
        qid2 = int(l_row_2[0])
        
        if qid1 not in d1:
            d1[qid1] = []
        d1[qid1].append(l_row_1)
            
        if qid2 not in d2:
            d1[qid2] = []
        d2[qid2].append(l_row_2)
        
    
    for k_text, k_title in
        
     
    
    return

def parse_line(row):
    l_row = row.split("\t")
    return [int(l_row_[1]), int(l_row_[2]), float(l_row_[3])]

main()
