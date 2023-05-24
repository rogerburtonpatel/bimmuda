# bimmuda

This repository primarily contains Bimmuda quantization scripts and output data.

These scripts are meant to be run in a pipeline with [idyom](https://github.com/mtpearce/idyom): \
You'll run the lyricstoints.py on your dataset, once to produce an output file \
and once to populate an output directory. You'll load the output file to \
an idyom database, run your desired commands, and produce an output file \
as a .csv. vis.ipynb can visualize the .csv files by sorting them by year \
based on the populated output directory. 


### Simple pipeline
Run `python lyricstoints.py` for quantization. By default, this will create \
a new directory and a new file in the `data/` dir, each containing the new \
quantizations. See the script docstring for specific details on output  \
formatting. The most important thing is that the .txt file created can be  \
sent directly to IDYOM for processing (i.e. you can create a db with this file.) 

### Details
The script generates a set of quantizations, assinging a new integer to each \
unique word in set of all words in the input files. Using these quantizations, \
it creates new 'quantized lyric' files, with 1 per file in the input directory, \
s.t. each file is the quantized version of its parent. For example: 

If our only file in our input were:

`short-song.txt` \
{ \
    Hello, goodbye, hello, goodbye, stop! \
}

The generated quantization (live during runtime only) would be: \
{ \
    Hello: 1 \
    goodbye: 2 \
    hello: 3 \
    stop: 4 \
}

And the output file would read:

`quantizations_DATETIME/short-song.txt` \
{ \
    1 2 3 2 4 \
} 

As you can see, all punctuation is stripped, and capitalization is NOT ignored.

The output file (by default `quantizations_DATETIME.txt`) contains each \
quantized lyrical file *on a new line*. As such, it can be used freely \
(and immediately) with IDYOM as its own new database, like so:

`(idyom-db:import-data :txt "PATH/quantizations_DATETIME.txt" "My new Quantizations!" DBNUM)`

<br>

## vis.ipynb
This can be used after IDYOM is run to generate visualizations from the .csv \
you'll produce from IDYOM output. For example, if you run:

`(idyom:idyom 12 '(CPITCH) '(CPITCH) :models :both :output-path NEW_FILE.csv :detail 2)`

you can run whichever parts of vis.ipynb you want, depending on your needs, \
with NEW_FILE.csv as the top-level global variable `csv1` (or `csv2`!)

***Make sure to set the `pth` global variable as your output directory from 
   `lyricstoints.py`!!!***

<br>

### Future directions
I can add functionality for dumping the quantizations to a file as an optional
parameter to the script, if this is helpful. 