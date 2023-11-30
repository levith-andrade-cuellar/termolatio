# Subject: Spanish POS Tagger
# Method Source: https://melaniewalsh.github.io/Intro-Cultural-Analytics/05-Text-Analysis/Multilingual/Spanish/03-POS-Keywords-Spanish.html
# Sample Text Source: https://www.latimes.com/espanol/internacional/articulo/2023-11-28/rehen-israeli-liberada-describe-como-se-deterioraban-las-condiciones-de-cautiverio-con-hamas

# WARNING ---------------------------------------------------------------------- #
# This program depends on the spacy Python module. Please download before using. |
# For more information check the "Method Source" linked above.                   |
# ------------------------------------------------------------------------------ #

# ---------------------- #
# Step 1: Import Modules |
# ---------------------- #

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

# Input files.
inputFile = open('sample.txt', 'r')
input = inputFile.read()

# Output files.
outputPOS = open('sample.pos', 'w')
outputCHUNKS = open('sample.tchunk', 'w')

# ----------------------- #
# Step 4: Processing Text |
# ----------------------- #

# Create a processed spaCy document.
document = nlp(input)

# --------------------------- #
# Step 5: Extract Information |
# --------------------------- #

# Using the processed spaCy document (an object),

# For each word in the document,
for token in document:
    # We output its lemmatized version and part of speech tag.
    outputPOS.write(f"{token.lemma_}\t{token.pos_}\n")

# For each chunk in the document,
for chunk in document.noun_chunks:
    # We output the chunk.
    outputCHUNKS.write(f"{chunk.text}\n")