# Subject: Noun Chunker
# Method Source: Adapted from the Chinese Version of the Termolator.

import argparse
import os

# INPUT (from background and foreground .pos files obtained in POS tagger) ----- #
# .pos file - from our POS tagger.                                               |
# ------------------------------------------------------------------------------ #

# OUTPUT ----------------------------------------------------------------------- #
# .pos file - in the format outline by the "print_pos" function.                 |
# .tchunk file - in the format outline by the "print_tchunk" function.           |
# ------------------------------------------------------------------------------ #

# --------- #
# Functions |
# --------- #

# ------------------------ #
# Function: Load Directory |
# ------------------------ #

# This function loads a directory into the program.

def load_directory(directory_name):
    return os.listdir(directory_name)

# ---------------------- #
# Function: Process Data |
# ---------------------- #

# This function takes as an input the name of a file (.pos).

def process_data(filename):
    # Open the file in read format.
    file = open(filename, 'r', encoding='UTF-8')
    # Prepare the result array which will contain smaller arrays of the form: [token, POS tag].
    result = []

    # For every line in the file, 
    for line in file:
        # Strip the line. 
        line = line.strip()
        # Split the line by a space.
        line_in_list = line.split(' ')

        # For every pair,
        for pair in line_in_list:
            # Split it based on a tab. 
            splited_pair = pair.split('\t') 
            # If the pair does not contain a POS tag we skip it.
            if len(splited_pair) < 2:
                continue
            # Otherwise we append the token and POS tag to the result list.
            result.append([splited_pair[0], splited_pair[1]])

    return result 

# ------------------------------------- #
# Function: BIO Tagging ("Detect Noun") |
# ------------------------------------- #

# This function takes as an input an array created from the "process_data" function. 
def detect_noun(pair_list):
    # Prepare the result array which will contain smaller arrays of the form: [token, tag, BIO_tag].
    result = [] 

    # For every pair "i" in the list,
    for i in range (len(pair_list)):
        
        # pair_list = [[token, POS tag], [token, POS tag], [token, POS tag], . . . ]

        # Only interested in nouns and adjectives.

        # ------------- #
        # Noun Detected |
        # ------------- #

        # If (read POS tag) is noun,
        if is_noun(pair_list[i][1]):

            # If the noun is the first word in the list of terms,                              
            if i == 0:
                # The noun must be at the beggining of the noun phrase.                                                       
                result.append([pair_list[i][0], pair_list[i][1], 'B-NP'])

            # If the noun is not the first word in the list of terms AND the previous word is in phrase (B-NP or I-NP),
            elif i > 0 and is_inword(result[i - 1][2]) == True:
                # The noun must be inside the noun phrase (I-NP).            
                result.append([pair_list[i][0], pair_list[i][1], 'I-NP'])

            # Otherwise,
            else:              
                # The noun must be the first word in the noun phrase.
                result.append([pair_list[i][0], pair_list[i][1], 'B-NP'])
        
        # ------------------ #
        # Adjective Detected |
        # ------------------ #

        # If (read POS tag) is adjective,                                    
        elif is_adj(pair_list[i][1]):

            # If the adjective is not the first word in the the list of terms AND the previous word is in phrase (B-NP or I-NP),
            if i > 0 and is_inword(result[i - 1][2]):                        
                # The word must be inside the noun phrase (I-NP).
                result.append([pair_list[i][0], pair_list[i][1], 'I-NP'])

            # Otherwise,
            else:
                # The adjective must be the first word in the noun phrase.
                result.append([pair_list[i][0], pair_list[i][1], 'B-NP'])

        # --------------------------- #
        # Non-Noun/Adjective Detected |
        # --------------------------- #
    
        else:
            # The word must be outside of the noun phrase.
            result.append([pair_list[i][0], pair_list[i][1], 'O'])

    return result

# -------------------- #
# Function: Is In Word |
# -------------------- #

# Identifies if a word is in a noun phrase.

def is_inword(BIOtag):
    inword_tag_set = set(['B-NP', 'I-NP'])
    if BIOtag in inword_tag_set:
        return True
    else:
        return False

# ---------------------- #
# Function: Is Adjective |
# ---------------------- #

# Identifies if a word is an adjective.
# Adjusted for the Spanish POS tag 'ADJ'.

def is_adj(tag):
    adj_tag_set = set(["ADJ"])
    return True if tag in adj_tag_set else False

# ----------------- #
# Function: Is Noun |
# ----------------- #

# Identifies if a word is a noun.
# Adjusted for the Spanish POS tag 'NOUN'.

def is_noun(tag):
    noun_tag_set = set(["NOUN"])
    return True if tag in noun_tag_set else False

# --------------------------- #
# Functions: Write Into Files |
# --------------------------- #

# Outputs the results into an output file. 

def print_tchunk(filename, tagged_words):
    file = open(filename, 'w', encoding= "UTF-8")
    for tagged_word in tagged_words:
        # Follow the CONLL format:
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

# ---------------------------- #
# Functions: String to Boolean |
# ---------------------------- #

# This function returns a corresponding boolen variable.

def str_to_bool(s):
    if s == 'True':
         return True
    elif s == 'False':
         return False
    else:
         raise ValueError

if __name__ == "__main__":

    # -------------------------------- #
    # Defining the Program's Arguments |
    # -------------------------------- #

    # Load the parser.
    parser = argparse.ArgumentParser(description="Outputting .tchunk and .pos files. A list of the tchunk names will be provided as well.")

    # Argument (-f): Foreground Directory
    parser.add_argument('-f', '--foreground', nargs = 1, help = "Please enter the input foreground directory", required = True)

    # Argument (-b): Background Directory
    parser.add_argument('-b', '--background', nargs = 1, help = "Please enter the input background directory", required = True)

    # Argument (-p): Program Directory
    parser.add_argument('-p','--program_directory',nargs=1,default=".",help="This should be the directory containing program files",required=True)

    # Parse the arguments and store them.
    args = parser.parse_args()


    # --------------------- #
    # Necessary Directories |
    # --------------------- #

    # Load: Foreground Directory 
    foreground_files = load_directory(args.foreground[0])

    # Load: Background Directory
    background_files = load_directory(args.background[0])

    # Save Name: Program Directory
    # We don't need to load information from here.
    program_dir = args.program_directory[0]

    # Create Path: Output Foreground Directory 
    out_foreground_path = os.path.join(os.getcwd(), "output_foreground")

    # Create Path: Output Background Directory
    out_background_path = os.path.join(os.getcwd(), "output_background")

    print("The program is runing and analyzing model.")


    # If the Output Foreground Directory doesn't yet exist,
    if not os.path.exists(out_foreground_path):
        # Create the directory.
        os.mkdir(out_foreground_path)

    # If the Output Background Directory doesn't yet exist,
    if not os.path.exists(out_background_path):
        # Create the directory.
        os.mkdir(out_background_path)

    # If the Output Foreground Directory exists,
    if os.path.exists("foreground_tchunk_list"):
        # Open it.
        file = open("foreground_tchunk_list", 'w+')
        file.close()

    # If the Output Background Directory exists,
    if os.path.exists("background_tchunk_list"):
        # Open it.
        file = open("background_tchunk_list", "w+")
        file.close()


    # ------------ #
    # Main Program |
    # ------------ #

    # ------------------------- #
    # I. Process the Background |
    # ------------------------- #

    print("Writing into foreground.")

    # For every file (.pos) in the foreground file directory,
    for file in foreground_files:

        # Prepare output files:
        # - tchunk
        # - pos 
        out_tchunk_file = "./output_foreground/" + file + ".tchunk"
        out_pos_file = "./output_foreground/" + file + ".pos"

        # -------------------------------------------------------- #
        # Step 1: Create an array of sub-arrays: [token, POS tag]. |
        # -------------------------------------------------------- #
        processed_data = process_data(args.foreground[0] + '/' + file)

        # ---------------------------------------------------------------------------------------------- #
        # Step 2: Use the array from Step 1 to create an array of sub-arrays: [token, POS tag, BIO_tag]. |
        # ---------------------------------------------------------------------------------------------- #
        tagged_nouns = detect_noun(processed_data)

        # --------------------------------------------------------------- #
        # Step 3: Write the results of BIO tagging into the output files. |
        # --------------------------------------------------------------- #
        print_tchunk(out_tchunk_file, tagged_nouns)
        print_pos(out_pos_file, tagged_nouns)

        # ------------------------------------------------------------ #
        # Step 4: Aggregate the results for all pos files fed as input |
        # ------------------------------------------------------------ #
        to_write = open("foreground_tchunk_list", 'a+')
        to_write.write(out_tchunk_file + '\n')
        to_write.close()

    # -------------------------- #
    # II. Process the Foreground |
    # -------------------------- #

    # Follow the same four steps as above.

    print("Writing into background.")
    for file in background_files:
        out_tchunk_file = "./output_background/" + file + ".tchunk"
        out_pos_file = "./output_background/" + file + ".pos"
        processed_data = process_data(args.background[0] + '/' + file)
        tagged_nouns = detect_noun(processed_data)
        print_tchunk(out_tchunk_file, tagged_nouns)
        print_pos(out_pos_file, tagged_nouns)
        to_write = open("background_tchunk_list", 'a+')
        to_write.write(out_tchunk_file + '\n')
        to_write.close()

    print("Finished")
