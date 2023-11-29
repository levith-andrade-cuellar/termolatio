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

# Regular importing procedure.
filepath = 'spanish_sample_text.txt'
text = open(filepath, encoding='utf-8').read()

# ----------------------- #
# Step 4: Processing Text |
# ----------------------- #

# Create a processed spaCy document.
document = nlp(text)

# --------------------------- #
# Step 5: Extract Information |
# --------------------------- #

# Within the processed spaCy document,
for token in document:
    # We can extract its lemmatized version, part of speech tag and dependency information.
    print(token.lemma_, token.pos_, token.dep_)


# An example for extracting all nouns.
nouns = []

for token in document:
    if (token.pos_ == 'NOUN'):
        nouns.append(token.lemma_)

print(nouns)

# Counts how many times a noun appears in the list.
numberOfNouns = Counter(nouns)

# Organizes the above from most to least common.
print(numberOfNouns.most_common)

