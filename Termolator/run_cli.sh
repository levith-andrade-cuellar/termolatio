# command line interface (cli) for spanish termolator
# this calls ./run_termolator_spanish.sh 

# Usage Format:
# ./run_cli.sh 

# reach goal: allow users to input url for foreground and background to scrape
echo 'Welcome to Spanish Termolator:'
echo '
 _____ _____ ____  __  __ _   _ _        _  _____ __ ___  
|_   _| ____|  _ \|  \/  | | | | |      / \|_   _/_// _ \ 
  | | |  _| | |_) | |\/| | | | | |     / _ \ | | | | | | |
  | | | |___|  _ <| |  | | |_| | |___ / ___ \| | | | |_| |
  |_| |_____|_| \_\_|  |_|\___/|_____/_/   \_\_| |_|\___/ 
'

echo 'Termulatío is at your service!'
echo '
         __     
 _(\    |@@|  <( nlp4lyf )
(__/\__ \--/ __ 
   \___|----|  |   __
       \ }{ /\ )_ / _\
       /\__/\ \__O (__ 
      (--/\--)    \__/
      _)(  )(_
     `---'\'''\''---`

'

echo "Please specify your folder arguments below."

# prompt the user for input with default values
read -p "Enter results folder (enter for default): " results
results=${results:-results}

read -p "Enter cleaned background folder (enter for default): " background
background=${background:-platos_carne}

read -p "Enter cleaned foreground folder (enter for default): " foreground
foreground=${foreground:-platos_carne}

read -p "Enter Termolator folder (enter for default): " termolator
termolator=${termolator:-.}

echo -e "Input complete"
# Run the command with user input
./run_termolator_spanish.sh "$results" "$background" "$foreground" "$termolator"
echo
echo
echo
echo "     Termulatío is done cooking!"
echo
cat <<'EOF'
 __       ___,.-------..__         __
//\\ _,-''_   _ _     ____ `'--._ //\\
\\ ;'    |  \| | |   |  _ \      `: //
 `(      | |\  | |___|  __/        )'
   :.    |_| \_|_____|_|         ,;
    `.`--.___           ___.--','
      `.     ``-------''     ,'
         -.               ,-
            `-._______.-'
EOF
echo
echo "Please check your results.out_term_list and the results.all_terms as the output files."
echo "Thank you for using Spanish Termolator!"