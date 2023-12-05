# Authors: Pauline Wee, Jhon Kim, Levith Andrade Cuellar 
# Date: November 28, 2023
# Description: Script to run the Spanish version of the Termolator.
# Usage Format: 
# bash run_Termolator_spanish.sh results cleaned/background cleaned/foreground .
# $1 = desired_output_name
# $2 = foreground directory
# $3 = background directory
# $4 = Termolator directory
echo
echo -e "Step 1 : Tagging using  Spanish POS tagger"
# create directories for POS tagged files
DIR=$1_tagged
if [ -d "$DIR" ]; then
    rm -r $DIR
    echo "Old $DIR removed!"
fi
mkdir $1_tagged
mkdir $1_tagged/background/
mkdir $1_tagged/foreground/

# Run Spanish Noun Chunker
python3 $4/spanish_pos_tagger.py -input $1_cleaned/background/ -output $1_tagged/background
python3 $4/spanish_pos_tagger.py -input $1_cleaned/foreground/ -output $1_tagged/foreground

echo -e "Step 2 : Noun Chunker Generator\nGenerating .tchunk and .pos files for the distributional ranking..."
# noun_chunker_generator.py implemented by Leizhen
python3 $4/spanish_noun_chunker_generator.py -f $1_tagged/foreground -b $1_tagged/background #-d $1 -p $5 <- $1 is for chinese dict & $5 for text file chinese1.txt

echo

echo -e "Step 3 : Distributional ranking\nGenerating .tchunk and .pos files for the distributional ranking...\n"
# MEASURES = ['TFIDF', 'DRDC', 'KLDiv', 'Weighted'] , same as English version
ls -1 output_foreground/ | grep "tchunk$" | awk '{print "output_foreground/"$1}' > $1.internal_foreground_tchunk_list
ls -1 output_background/ | grep "tchunk$" | awk '{print "output_background/"$1}' > $1.internal_background_tchunk_list
python3 $4/distributional_component.py NormalRank $1.internal_foreground_tchunk_list $1.all_terms False $1.internal_background_tchunk_list

# echo -e "Step 4 : Accessor Variety Filter\nFiltering all terms obtained previously...\n"
# python3 $5/accessorvariety.py $2.all_terms foreground_tchunk_list > $2.AV_filtered_terms
# echo -e "All steps completed! Final output file: $2.AV_filtered_terms"

cut -f 1 $1.all_terms > $1.out_term_list

