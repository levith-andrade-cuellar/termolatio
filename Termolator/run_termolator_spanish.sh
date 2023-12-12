#!/bin/bash

# Authors: Pauline Wee, Jhon Kim, Levith Andrade Cuellar 
# Date: November 28, 2023
# Description: Script to run the Spanish version of the Termolator.
# Usage Format: 
#  ./run_termolator_spanish.sh results cleaned/background cleaned/foreground .
# $1 = desired_output_name
# $2 = foreground directory
# $3 = background directory
# $4 = Termolator directory

echo
echo -e "Step 1 : Tagging using  Spanish POS tagger"
# create directories for POS tagged files
# for item in $1_tagged $1.internal_foreground_tchunk_list $1.internal_background_tchunk_list output_foreground output_background ; do
#     if [ -f "$item" ]; then
#         rm "$item"  # Remove file
#     elif [ -d "$item" ]; then
#         rm -r "$item"  # Remove directory and its contents
#     fi
# done


mkdir $1_tagged
mkdir $1_tagged/background/
mkdir $1_tagged/foreground/

# Run Spanish Noun Chunker
input_directory1="$3/background/"
output_directory="$1_tagged"
input_directory2="$2/foreground/"
pos_tagger_script="$4/spanish_pos_tagger.py"

python ./spanish_pos_tagger.py --foreground $input_directory2 --background $input_directory1 --output $output_directory 

echo -e "Step 2 : Noun Chunker Generator\nGenerating .tchunk and .pos files for the distributional ranking..."
# noun_chunker_generator.py implemented by Leizhen
python $4/spanish_noun_chunker_generator.py -f $1_tagged/foreground -b $1_tagged/background -p $4 #-d $1 -p $5 <- $1 is for chinese dict & $5 for text file chinese1.txt

echo

echo -e "Step 3 : Distributional ranking\nGenerating .tchunk and .pos files for the distributional ranking...\n"
# MEASURES = ['TFIDF', 'DRDC', 'KLDiv', 'Weighted'] , same as English version
ls -1 output_foreground/ | grep "tchunk$" | awk '{print "output_foreground/"$1}' > $1.internal_foreground_tchunk_list
ls -1 output_background/ | grep "tchunk$" | awk '{print "output_background/"$1}' > $1.internal_background_tchunk_list
python $4/distributional_component.py NormalRank $1.internal_foreground_tchunk_list $1.all_terms False $1.internal_background_tchunk_list
cut -f 1 $1.all_terms > $1.out_term_list