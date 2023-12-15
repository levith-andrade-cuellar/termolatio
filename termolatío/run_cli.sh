# command line interface (cli) for spanish termolator
# this calls ./run_termolator_spanish.sh 

# Usage Format:
# ./run_cli.sh 

# reach goal: allow users to input url for foreground and background to scrape
echo
echo
echo
echo '       Welcome to Spanish Termolator:'
cat <<'EOF'
 _                           _       _    __      
| |_ ___ _ __ _ __ ___   ___ | | __ _| |_/_/ ___  
| __/ _ \ '__| '_ ` _ \ / _ \| |/ _` | __| |/ _ \ 
| ||  __/ |  | | | | | | (_) | | (_| | |_| | (_) |
 \__\___|_|  |_| |_| |_|\___/|_|\__,_|\__|_|\___/ 
EOF
echo
echo '      termolatío is at your service!'
cat <<'EOF'
                     __     
             _(\    |@@|  <( nlp4lyf )
            (__/\__ \--/ __ 
               \___|----|  |   __
                   \ }{ /\ )_ / _\
                   /\__/\ \__O (__ 
                  (--/\--)    \__/
                  _)(  )(_
                `---'' '---`

EOF

echo "Please specify your folder arguments below."

# prompt the user for input with default values
read -p "Enter results folder (enter for default): " results
results=${results:-results}

read -p "Enter cleaned background folder (enter for default): " background
background=${background:-tech}

read -p "Enter cleaned foreground folder (enter for default): " foreground
foreground=${foreground:-tech}

read -p "Enter Termolator folder (enter for default): " termolator
termolator=${termolator:-.}

echo -e "Input complete"
# Run the command with user input
./run_termolator_spanish.sh "$results" "$background" "$foreground" "$termolator"
echo
echo
echo
echo "      termolatío is done cooking!"
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