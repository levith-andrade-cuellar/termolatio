# Authors: Pauline Wee, Jhon Kim, Levith Andrade Cuellar 
# Date: November 28, 2023
# Description: Script to run the Spanish version of the Termolator.
# Usage Format: 
# run_termolator_spanish.sh True desired_output_name cleaned/foreground cleaned/background Termulator True

echo
echo -e "Step 1 : Tagging using Brandeis tagger\nRunning Brandeis Chinese word segmenter and part-of-speech tagger..."
# create directories for POS tagged files
DIR=$2_tagged
if [ -d "$DIR" ]; then
    rm -r $DIR
    echo "Old $DIR removed!"
fi
mkdir $2_tagged
mkdir $2_tagged/background/
mkdir $2_tagged/foreground/

# Run Brandeis Chinese word segmenter and part-of-speech tagger
## cd $5/Brandeis-CASIA-LanguageProcesser
python3 $5/spanish_noun_chunker_generator.py -input $2_cleaned/background/ -output $2_tagged/background
python3 $5/spanish_noun_chunker_generator.py -input $2_cleaned/foreground/ -output $2_tagged/foreground

echo -e "Step 2 : Noun Chunker Generator\nGenerating .tchunk and .pos files for the distributional ranking..."
# noun_chunker_generator.py implemented by Leizhen
python3 $5/spanish_noun_chunker_generator.py -f $2_tagged/foreground -b $2_tagged/background -d $1 -p $5
echo

echo -e "Step 3 : Distributional ranking\nGenerating .tchunk and .pos files for the distributional ranking...\n"
# MEASURES = ['TFIDF', 'DRDC', 'KLDiv', 'Weighted'] , same as English version
ls -1 output_foreground/ | grep "tchunk$" | awk '{print "output_foreground/"$1}' > $2.internal_foreground_tchunk_list
ls -1 output_background/ | grep "tchunk$" | awk '{print "output_background/"$1}' > $2.internal_background_tchunk_list
python3 $5/distributional_component.py NormalRank $2.internal_foreground_tchunk_list $2.all_terms False $2.internal_background_tchunk_list

# echo -e "Step 4 : Accessor Variety Filter\nFiltering all terms obtained previously...\n"
# python3 $5/accessorvariety.py $2.all_terms foreground_tchunk_list > $2.AV_filtered_terms
# echo -e "All steps completed! Final output file: $2.AV_filtered_terms"

cut -f 1 $2.all_terms > $2.out_term_list

