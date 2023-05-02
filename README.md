# bimmuda

This repository primarily contains Bimmuda quantization scripts and output data.

These scripts are meant to be run in a pipeline with [idyom](https://github.com/mtpearce/idyom):
You'll run the lyricstoints.py on your dataset, once to produce an output file 
and once to populate an output directory. You'll load the output file to 
an idyom database, run your desired commands, and produce an output file 
as a .csv. vis.ipynb can visualize the .csv files by sorting them by year
based on the populated output directory. 

python lyricstoints.py for quantization. 