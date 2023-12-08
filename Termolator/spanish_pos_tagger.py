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
import argparse
import os

# ---------------------- #
# Step 2: Load spacy     |
# ---------------------- #
nlp = spacy.load('es_core_news_md')

# ---------------------- #
# Step 3: Load directory |
# ---------------------- #
def process_directory(input_dir, output_dir):
    for filename in os.listdir(input_dir):
        if not filename.endswith('.txt'):
            continue  # skiping non-txt files e.g. .DS_Store

        input_file_path = os.path.join(input_dir, filename)
        tagged_text = pos_tag_file(input_file_path)

        # remove .txt extension from filename before appending .pos
        output_filename = filename[:-4] + '.pos'
        output_file_path = os.path.join(output_dir, output_filename)

        with open(output_file_path, 'w', encoding='UTF-8') as output_file:
            for word, tag in tagged_text:
                output_file.write(f"{word}\t{tag}\n")

# ---------------------- #
# Step 4: POS tagging    |
# ---------------------- #
def pos_tag_file(file_path):
    with open(file_path, 'r', encoding='UTF-8') as file:
        text = file.read()
        doc = nlp(text)
        return [(token.text, token.pos_) for token in doc]

# ---------------------- #
#    Loading arguments   |
# ---------------------- #
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="POS Tagging for Foreground and Background directories.")
    parser.add_argument('-f', '--foreground', required=True, help="Input directory for foreground files")
    parser.add_argument('-b', '--background', required=True, help="Input directory for background files")
    parser.add_argument('-o', '--output', required=True, help="Output directory for tagged results")
    args = parser.parse_args()

    foreground_input_dir = args.foreground
    background_input_dir = args.background
    output_dir = args.output

    foreground_output_dir = os.path.join(output_dir, "foreground")
    background_output_dir = os.path.join(output_dir, "background")

    os.makedirs(foreground_output_dir, exist_ok=True)
    os.makedirs(background_output_dir, exist_ok=True)

    process_directory(foreground_input_dir, foreground_output_dir)
    process_directory(background_input_dir, background_output_dir)

    print("Finished POS tagging for foreground and background directories.")