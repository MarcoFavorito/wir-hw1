def file2dict_qid(file, formats):
    """

    :param file: file tab-separated-value format
    :param formats: a list of function String => Type
    :return: a dictionary as key the query ids and as value the list of tuples.
    """

    def add_to_dict(tuple, d):
        """

        :param tuple: (key, value1, value2...)
        :param d: dictionary on which we will do side-effect
        :return: d
        """
        qId = tuple[0]
        if qId not in d.keys():
            d[qId] = []
        if len(tuple)==2:
            d[qId].append(tuple[1])
        else:
            d[qId].append(tuple[1:])

    res = {}
    text = file.read()

    for line in text.splitlines()[1:]:
        add_to_dict(parse_line(line, formats),res)

    return res


def file2list(file, formats):
    l = [parse_line(line, formats) for line in file.read().splitlines()]
    return l


def parse_line(line, formats):
    return [formats[i](value) for i, value in enumerate(line.split("\t"))]