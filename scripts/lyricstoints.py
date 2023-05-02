#! /Users/rogerburtonpatel/opt/anaconda3/bin/python

# current canonical script for generating mappings. 

from pathlib import Path
import itertools
from string import punctuation
# for use in IDYOM at mtpearce/idyom/wiki
# auth Roger Burtonpatel

# type aliases
Name            = str
Quantization    = list[int]
Quantized_files = dict[Name:Quantization]
Lyric_mapping   = dict[str:int]

INPUT_PATH = "/Users/rogerburtonpatel/home/london/bimmuda/bimmuda_lyrics/"
OUTPUT_DIR = "/Users/rogerburtonpatel/home/london/bimmuda/quantizations-by-decade/" 
OUTPUT_FILE = "/Users/rogerburtonpatel/home/london/bimmuda/quantizations-by-decade.txt" 
# must end with /

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

def quantizeWithAllFiles(p: Path, output: str):
    files = sorted(list(p.glob('*lyrics.txt')))
    _, quantizations = mapAndQuantize(files)

    # output format:
    # 1 file, 1 line per song, space-sperated integers (lyrics)
    if output[-1] == "/":
        for filename, quantization in quantizations.items():
            with open(output + filename, "w") as outfile:
                for num in quantization:
                    outfile.write(str(num) + ' ')
    else:
        with open(output, "w") as outfile: 
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

def quantizeByDecade(p: Path, output: str):
    decades = makeDecades(p)
    if output[-1] == "/":
        for decade, files in decades.items():
            _, quantizations = mapAndQuantize(files)
            for filename, quantization in quantizations.items():
                with open(output + filename, "w") as outfile:
                    for num in quantization:
                        outfile.write(str(num) + ' ')
    else:
        with open(output, "w") as outfile:
            for decade, files in decades.items():
                _, quantizations = mapAndQuantize(files)
                for filename, quantization in quantizations.items():
                    for num in quantization:
                        outfile.write(str(num) + ' ')
                    outfile.write('\n ')
                
def main():
    p = Path(INPUT_PATH) # you could make this an argument
    quantizeByDecade(p, OUTPUT_DIR)

if __name__ == "__main__":
    main()