# Phoneme Discovery

This repository contains the pipeline used to produce the results in Fourtassi, Dunbar & Dupoux (in prep.). 

To reproduce the results, run the bash code in "run.sh" using a terminal.

First, you need to install the python library "Gensim".

The code takes two arguments:
1) a language: 'Eng' or 'Jap' (for English and Japanese)
2) a segmentation type: 'gold', 'seg' or 'rand' (which stand for ideal, unsupervised and random)

For example, the folowing command line computes the differentiation score for English using unsupervised segmentation:

./run.sh Eng seg

The output goes to the folder "res".
