def find_and_replace_in_text_phrase_one_with_phrase_two(txt, phrase_one, phrase_two):
    txt.replace(phrase_one, phrase_two)

def get_txt_from_file(file_name):
    file = open(file_name, "r")
    lines = file.readlines()
    txt = ""
    for str in lines:
        txt += str + " "
    return txt

def convert_list_of_list_of_tuples_to_list_of_lists(list_of_list_of_tuples):
    return_list = []
    for list_of_tuples in list_of_list_of_tuples:
        clause_list = []
        for tuple in list_of_tuples:
            list = []
            for item in tuple:
                list.append(item)
            clause_list.append(list)
        return_list.append(clause_list)
    return return_list

if __name__ == "__main__":
    pass