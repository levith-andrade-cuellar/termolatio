'''
Jhon
'''

import argparse
import os


def load_directory(directory_name):
    return os.listdir(directory_name)


def process_data(filename):
    file = open(filename, 'r', encoding='UTF-8')
    result = []
    for line in file:
        line = line.strip()
        line_in_list = line.split(' ') # change the line into a list by space
        for pair in line_in_list:
            splited_pair = pair.split('\t') # change 本_DT to [‘本’, DT]
            # print("this is the splitted pair", splited_pair)
            if len(splited_pair) < 2:
                continue
            result.append([splited_pair[0], splited_pair[1]])
    return result #result is a list of pairs with information word at first followed by the information

#If anyone wants to change the rules for detecting the term, this method is a good way to start
def detect_noun(pair_list):
    result = [] # information stored in the format of [word, tag, BIO_tag]
    for i in range (len(pair_list)):

        if is_noun(pair_list[i][1]): # detect the noun first
            if i == 0: # The first of the word is 0
                result.append([pair_list[i][0], pair_list[i][1], 'B-NP'])
            elif i > 0 and is_inword(result[i - 1][2]) == True: # check if the previous word is in_word
                result.append([pair_list[i][0], pair_list[i][1], 'I-NP'])
            else: # if this noun is the start, then it will be in_word
                result.append([pair_list[i][0], pair_list[i][1], 'B-NP'])
        elif is_adj(pair_list[i][1]): # if an adj is detected, then it will be the start of the term
            if i > 0 and is_inword(result[i - 1][2]): # check if the previous word is in_word
                result.append([pair_list[i][0], pair_list[i][1], 'I-NP'])
            else:
                result.append([pair_list[i][0], pair_list[i][1], 'B-NP'])
        else:
            result.append([pair_list[i][0], pair_list[i][1], 'O'])
    return result

def print_tchunk(filename, tagged_words):
    file = open(filename, 'w', encoding= "UTF-8")
    for tagged_word in tagged_words: # follow the CONLL format
        file.write(tagged_word[0]+"\t\t"+tagged_word[0]+"\t\t"+tagged_word[1]+"\t\t"+tagged_word[2]+"\n")
    file.close()

def print_pos(filename, tagged_words):
    start_point = 1
    file = open(filename, 'w', encoding= "UTF-8")
    for tagged_word in tagged_words:
        end_point = start_point + len(tagged_word[0])
        file.write(tagged_word[0] + "\t|||\tS: " + str(start_point) + "E: " + str(end_point) + "\t|||\t" + tagged_word[1] + "\n")
        start_point = end_point
    file.close()

def is_inword(BIOtag):
    inword_tag_set = set(['B-NP', 'I-NP'])
    if BIOtag in inword_tag_set:
        return True
    else:
        return False

def is_adj(tag):
    adj_tag_set = set(["ADJ"])
    return True if tag in adj_tag_set else False

def is_noun(tag):
    noun_tag_set = set(["NOUN"])
    return True if tag in noun_tag_set else False

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Outputting .tchunk and .pos files. A list of the tchunk names will be provided as well.")
    parser.add_argument('-f', '--foreground', nargs = 1, help = "Please enter the input foreground directory", required = True)
    parser.add_argument('-b', '--background', nargs = 1, help = "Please enter the input background directory", required = True)
    parser.add_argument('-p','--program_directory',nargs=1,default=".",help="This should be the directory containing program files",required=True)
    args = parser.parse_args()

    foreground_files = load_directory(args.foreground[0])
    background_files = load_directory(args.background[0])
    program_dir = args.program_directory[0]

    out_foreground_path = os.path.join(os.getcwd(), "output_foreground")
    out_background_path = os.path.join(os.getcwd(), "output_background")

    print("The program is runing and analyzing model.")

    if not os.path.exists(out_foreground_path):
        os.mkdir(out_foreground_path)
    if not os.path.exists(out_background_path):
        os.mkdir(out_background_path)

    if os.path.exists("foreground_tchunk_list"):
        file = open("foreground_tchunk_list", 'w+')
        file.close()
    if os.path.exists("background_tchunk_list"):
        file = open("background_tchunk_list", "w+")
        file.close()
    #output files from foreground

    print("Writing into foreground.")
    for file in foreground_files:
        out_tchunk_file = "./output_foreground/" + file + ".tchunk"
        out_pos_file = "./output_foreground/" + file + ".pos"
        processed_data = process_data(args.foreground[0] + '/' + file)
        tagged_nouns = detect_noun(processed_data)
        print_tchunk(out_tchunk_file, tagged_nouns)
        print_pos(out_pos_file, tagged_nouns)

        # if (dict_on == True):
        #     dict_filter(tagged_nouns,program_dir)


        to_write = open("foreground_tchunk_list", 'a+')
        to_write.write(out_tchunk_file + '\n')
        to_write.close()

    print("Writing into background.")
    for file in background_files:
        out_tchunk_file = "./output_background/" + file + ".tchunk"
        out_pos_file = "./output_background/" + file + ".pos"
        processed_data = process_data(args.background[0] + '/' + file)
        tagged_nouns = detect_noun(processed_data)
        print_tchunk(out_tchunk_file, tagged_nouns)
        print_pos(out_pos_file, tagged_nouns)
        # if (dict_on == True):
        #      dict_filter(tagged_nouns,program_dir)


        to_write = open("background_tchunk_list", 'a+')
        to_write.write(out_tchunk_file + '\n')
        to_write.close()

    print("Finished")
