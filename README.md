# PhonemeDiscovery

This repositor contains the pipeline used to produce results in Fourtassi, Dunbar & Dupoux (in prep.). 

An earlier version of this project was published as Fourtassi, Dunbar & Dupoux (2014). CogSci.

To reproduce the results, run the bash code in run.sh in a terminal.

The only dependency you need to install is the python library "Gensim".

The code takes two arguments:
1) a languag: 'Eng' or 'Jap' (for English and Japanese)
2) a segmentation type: 'gold', 'seg' or 'rand' (which stand for ideal, unsupervised and random)

Example, the folowing line command compute the differentiation score for English using unsupervised segmentation:

./run.sh Eng seg
