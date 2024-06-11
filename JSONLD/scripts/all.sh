#! /bin/bash 

python update_new.py;

./combine_graphs.sh compiled/graph_data .. graph ../miptables

# ./combine_graphs.sh compiled/data_request ../miptables graph none
# ./combine_graphs.sh compiled/versioning .. version none

# Directory containing the files
DIR="node_scripts"

# Loop through each file in the directory
for FILE in "$DIR"/*
do
  # Check if it is a file (not a directory)
  if [ -f "$FILE" ]; then
    # Run your command here, e.g., print the file name
    echo "Processing file: $FILE"
    # skip files that start with x
        if [[ "$filename" != x* ]]; then
    node $FILE
    fi
    
    # Example command: Run a script or command with the file as an argument
    # ./your_command "$FILE"
  fi
done

