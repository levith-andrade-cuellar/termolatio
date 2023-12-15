# Subject: Spanish POS Tagger
# Method Source: https://melaniewalsh.github.io/Intro-Cultural-Analytics/05-Text-Analysis/Multilingual/Spanish/03-POS-Keywords-Spanish.html
# Sample Text Source: https://www.latimes.com/espanol/internacional/articulo/2023-11-28/rehen-israeli-liberada-describe-como-se-deterioraban-las-condiciones-de-cautiverio-con-hamas

# WARNING ---------------------------------------------------------------------- #
# This program depends on the spacy Python module. Please download before using. |
# For more information check the "Method Source" linked above.                   |
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

# ------------------ #
# Step 2: Load Spacy |
# ------------------ #
nlp = spacy.load('es_core_news_md')

# --------------------- #
# Function: POS Tagging |
# --------------------- #
def pos_tag_file(file_path):
    with open(file_path, 'r', encoding='UTF-8') as file:
        text = file.read()
        doc = nlp(text)
        return [(token.text, token.pos_) for token in doc]

# -------------------------------------- #
# Step 3: POS Tag All Files in Directory |
# -------------------------------------- #
def process_directory(input_dir, output_dir):

    # For file in directory,
    for filename in os.listdir(input_dir):
        if not filename.endswith('.txt'):
            continue  # Skiping non-txt files (e.g. .DS_Store)

        input_file_path = os.path.join(input_dir, filename)

        # Tag the text in the input file. 
        tagged_text = pos_tag_file(input_file_path)

        # Remove .txt extension from filename before appending .pos
        output_filename = filename[:-4] + '.pos'

        # Create Path: Output File
        output_file_path = os.path.join(output_dir, output_filename)

        # Write into the output file the following,
        with open(output_file_path, 'w', encoding='UTF-8') as output_file:

            # For every word and tag in the tagged text.
            for word, tag in tagged_text:

                # Write those to the output file separated by a tab.
                output_file.write(f"{word}\t{tag}\n")


if __name__ == "__main__":

    # -------------------------------- #
    # Defining the Program's Arguments |
    # -------------------------------- #

    # Load the parser.
    parser = argparse.ArgumentParser(description="POS Tagging for Foreground and Background directories.")

    # Argument (-f): Foreground Directory
    parser.add_argument('-f', '--foreground', required=True, help="Input directory for foreground files")

    # Argument (-b): Background Directory
    parser.add_argument('-b', '--background', required=True, help="Input directory for background files")

    # Argument (-o): Output Directory
    parser.add_argument('-o', '--output', required=True, help="Output directory for tagged results")

    # Parse the arguments and store them.
    args = parser.parse_args()

    # --------------------- #
    # Necessary Directories |
    # --------------------- #

    # Save Name: Foreground Input Directory
    foreground_input_dir = args.foreground

    # Save Name: Background Input Directory
    background_input_dir = args.background

    # Save Name: Output Directory
    output_dir = args.output

    # Create Path: Output Foreground Directory 
    foreground_output_dir = os.path.join(output_dir, "foreground")

    # Create Path: Output Background Directory 
    background_output_dir = os.path.join(output_dir, "background")

    # Create the Foreground Output Directory
    os.makedirs(foreground_output_dir, exist_ok=True)

    # Create the Background Output Directory
    os.makedirs(background_output_dir, exist_ok=True)

    # Process the directory, iterate through its files.
    process_directory(foreground_input_dir, foreground_output_dir)
    process_directory(background_input_dir, background_output_dir)

    print("Finished POS tagging foreground and background directories.")