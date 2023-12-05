# Subject: Spanish Noun Chunker Tagger
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
# .tchunk file - containing all noun chunks found in the text.                   |
# ------------------------------------------------------------------------------ #

# ---------------------- #
# Step 1: Import Modules |
# ---------------------- #
import sys
import spacy
from spacy import displacy
from collections import Counter

# --------------------------- #
# Step 2: Load Language Model |
# --------------------------- #

nlp = spacy.load('es_core_news_md')

# ------------------- #
# Step 3: Import Text |
# ------------------- #

# Input file, use the one indicated by the argument.
inputFile = open(sys.argv[1], 'r') 
input = inputFile.read()

# Output files.
outputCHUNKS = open(f'{sys.argv[1][:-4]}.tchunk', 'w')

# -------------------- #
# Step 4: Process Text |
# -------------------- #

# Create a processed spaCy document.
document = nlp(input)

# --------------------------- #
# Step 5: Extract Information |
# --------------------------- #

# Using the processed spaCy document (an object),

# For each chunk in the document,
for chunk in document.noun_chunks:
    # We output the chunk.
    outputCHUNKS.write(f"{chunk.text}\n")