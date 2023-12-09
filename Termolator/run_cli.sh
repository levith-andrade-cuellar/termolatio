# command line interface (cli) for spanish termolator
# this calls ./run_termolator_spanish.sh 

# Usage Format:
# ./run_cli.sh 

# reach goal: allow users to input url for foreground and background to scrape

echo "\nWelcome to Spanish Termolator!\n"

echo '       termulatio
  is at your service!

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

echo "Please specify your folder arguments below.\n"

# Prompt the user for input with default values
read -p "Enter results folder (enter for default): " results
results=${results:-results}

read -p "Enter cleaned background folder (enter for default): " background
background=${background:-cleaned/background}

read -p "Enter cleaned foreground folder (enter for default): " foreground
foreground=${foreground:-cleaned/foreground}

read -p "Enter Termolator folder (enter for default): " termolator
termolator=${termolator:-.}

echo -e "Input complete"
# Run the command with user input
./run_termolator_spanish.sh "$results" "$background" "$foreground" "$termolator"