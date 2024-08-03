#! /bin/bash 

python update_new.py $@;

./combine_graphs.sh compiled/graph_data .. graph ../scripts 

# if using flags.

