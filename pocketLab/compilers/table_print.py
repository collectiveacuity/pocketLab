__author__ = 'rcj1492'
__created__ = '2016.03'

def tablePrint(header_list, dict_list):

    print_string = ''

# determine separation spacing based upon max character length
    max_lengths = {}
    for field in header_list:
        max_lengths[field] = len(field)
    for row in dict_list:
        for key, value in row.items():
            if key in max_lengths.keys():
                if len(str(value)) > max_lengths[key]:
                    max_lengths[key] = len(str(value))

# create columns from header list
    for field in header_list:
        print_string += field
        spacing = max_lengths[field] - len(field)
        count = 0
        while count < spacing + 3:
            print_string += ' '
            count += 1
    print_string += '\n'

# add row values
    for row in dict_list:
        for field in header_list:
            spacing = max_lengths[field]
            if field in row.keys():
                print_string += str(row[field])
                spacing = spacing - len(str(row[field]))
            count = 0
            while count < spacing + 3:
                print_string += ' '
                count += 1
        print_string += '\n'

    return print_string