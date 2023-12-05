# This bash file iterates through files in a folder and runs them through our POS tagger.

for file in /Users/levith/Desktop/termulador-sandbox/Termolator/cleaned/background/*.txt; do
    echo "Processing file: $file"
    python3 spanish_pos_tagger.py "$file"
done