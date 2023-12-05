# Subject: Spanish POS Tagger
# Method Source: https://melaniewalsh.github.io/Intro-Cultural-Analytics/05-Text-Analysis/Multilingual/Spanish/03-POS-Keywords-Spanish.html
# Sample Text Source: https://www.latimes.com/espanol/internacional/articulo/2023-11-28/rehen-israeli-liberada-describe-como-se-deterioraban-las-condiciones-de-cautiverio-con-hamas

# WARNING ---------------------------------------------------------------------- #
# This program depends on the spacy Python module. Please download before using. |
# For more information check the "Method Source" linked above.                   |
# ------------------------------------------------------------------------------ #

# HOW TO USE ------------------------------------------------------------------- #
# This program takes a single argument. It takes a .txt file containing cleaned  |
# text from our scraper.                                                         |
# ------------------------------------------------------------------------------ #

# INPUT (as an argument) ------------------------------------------------------- #
# .txt file - containing cleaned text from our scraper.                          |
# ------------------------------------------------------------------------------ #

# OUTPUT ----------------------------------------------------------------------- #
# .pos file - containing all tokens in the text and their corresponding POS tags |
# ------------------------------------------------------------------------------ #

# ---------------------- #
# Step 1: Import Modules |
# ---------------------- #
import sys
import spacy
# from spacy import displacy
# from collections import Counter

# --------------------------- #
# Step 2: Load Language Model |
# --------------------------- #

nlp = spacy.load('es_core_news_md')

# ------------------- #
# Step 3: Import Text |
# ------------------- #

# Input file, use the one indicated by the argument.
# inputFile = open(sys.argv[1], 'r') 
# input = inputFile.read()
input_file_path = sys.argv[1]
output_directory = sys.argv[2]
# print('this is the output directory', output_directory)

# output_file_path = Path(output_directory) / f'{Path(input_file_path).stem}.pos'


# Output files.
# outputPOS = open(f'{sys.argv[1][:-4]}.pos', 'w')
with open(input_file_path, 'r') as inputFile:
    input_text = inputFile.read()

# -------------------- #
# Step 4: Process Text |
# -------------------- #

# Create a processed spaCy document.
document = nlp(input_text)

# --------------------------- #
# Step 5: Extract Information |
# --------------------------- #

# Using the processed spaCy document (an object),

# For each word in the document,
# for token in document:
#     # We output the token and part of speech tag.
#     outputPOS.write(f"{token.text}\t{token.pos_}\n")
with open(output_directory, 'w') as outputPOS:
    for token in document:
        outputPOS.write(f"{token.text}\t{token.pos_}\n")