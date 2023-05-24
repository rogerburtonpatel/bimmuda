#! /usr/bin/python3

"""
current canonical script for generating quantizeds files. 
    Running this will generate quantizations: mappings from lyrics (words) to 
    integers. It will then use those mappings to generate 2 sets of output:
    1. a directory containing the quantized version of each lyric file in the 
    intput directory
    2. a file containing the quantized version of each lyric file on a new line
    (i.e. this contains ALL quantized lyrics, with one 'song' per line.)
   The file can be put directly into IDYOM for processing. 
"""

import argparse
import os
from pathlib import Path
from string import punctuation
from datetime import datetime

# for use in IDYOM at mtpearce/idyom/wiki
# auth Roger Burtonpatel

# type aliases
Name            = str
Quantization    = list[int]
Quantized_files = dict[Name:Quantization]
Lyric_mapping   = dict[str:int]

def mapAndQuantize(files: list[str]) -> tuple[Lyric_mapping,
                                              Quantized_files]:
    """takes a path to a directory containing one or more files of lyrics and
        returns the tuple of 
        (the dict of mappings {lyrics:number} for all songs, 
        the dict of 
            {songName: song represented as numbers according to the mappings})
    """

    allLyricsMapped = {}
    allQuantizations = {}

    for file in files:
        with file.open() as f:
            i = 0
            # get individual mappings/quantizations for each song
            quantization = []
            for line in f:
                for word in line.split():
                    # remove puncutation
                    word = word.strip(punctuation)
                    # map word to number and use that number for quantization
                    if not word in allLyricsMapped:
                        allLyricsMapped[word] = i
                    i += 1
                    quantization.append(allLyricsMapped[word])
        # add to 'global' accumulator 
        allQuantizations[file.name] = quantization

    return allLyricsMapped, allQuantizations

def quantizeWithAllFiles(p: Path, output_dir: str, output_file: str):
    files = sorted(list(p.glob('*lyrics.txt')))
    _, quantizations = mapAndQuantize(files)

    # output format within output_dir:
    # 1 file per song, space-sperated integers (lyrics)

    # need to mkdir to build output directory before populating
    os.makedirs(output_dir, exist_ok=True)
    for filename, quantization in quantizations.items():
        with open(os.path.join(output_dir, filename), "w") as outfile:
            for num in quantization:
                outfile.write(str(num) + ' ')
    
    # output format in output_file:
    # 1 file, 1 line per song, space-sperated integers (lyrics)
    with open(output_file, "w") as outfile: 
        for filename, quantization in quantizations.items():
            for num in quantization:
                outfile.write(str(num) + ' ')
            outfile.write('\n ')

def makeDecades(p: Path):
    files = sorted(list(p.glob('*lyrics.txt')))

    decades = {}
    for file in files:
        file_decade = (file.name[:3] + '0s')
        if not file_decade in decades:
            decades[file_decade] = [file]
        else:
            decades[file_decade].append(file)

    return decades

def quantizeByDecade(p: Path, output_dir: str, output_file: str):
    decades = makeDecades(p)

    # need to mkdir to build output directory before populating
    os.makedirs(output_dir, exist_ok=True)
    for decade, files in decades.items():
        _, quantizations = mapAndQuantize(files)
        for filename, quantization in quantizations.items():
            with open(os.path.join(output_dir, filename), "w") as outfile:
                for num in quantization:
                    outfile.write(str(num) + ' ')
    
    with open(output_file, "w") as outfile:
        for decade, files in decades.items():
            _, quantizations = mapAndQuantize(files)
            for filename, quantization in quantizations.items():
                for num in quantization:
                    outfile.write(str(num) + ' ')
                outfile.write('\n ')
                
def main():
    parser = argparse.ArgumentParser(
        description="Quantization of lyrics files for IDYOM analysis",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default="../bimmuda_lyrics/",
        help="Input text file or files.",
    )
    parser.add_argument(
        "-O",
        "--output_dir",
        type=str,
        # you may want to change these defaults if your directory 
        # is set up differently. 
        default="../data/quantizations_" + 
                    datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + "/", 
        help="Directory to contain quantizations. Need not exist yet.",
    )
    parser.add_argument(
        "-o",
        "--output_file",
        type=str,
        # you may want to change these defaults if your directory 
        # is set up differently. 
        default="../data/quantizations_" + 
                    datetime.now().strftime("%Y_%m_%d-%I_%M_%S_%p") + ".txt",
        help="File to contain quantizations. Need not exist yet.",
    )
    parser.add_argument(
        "-d",
        "--decades",
        help="Quantize using mappings per decade rather than global mappings",
        action="store_true",
    )

    args = parser.parse_args()

    p = Path(args.input)
    out_dir = args.output_dir
    out_file = args.output_file

    if args.decades:
        quantizeByDecade(p, out_dir, out_file)
    else:
        quantizeWithAllFiles(p, out_dir, out_file)

if __name__ == "__main__":
    main()