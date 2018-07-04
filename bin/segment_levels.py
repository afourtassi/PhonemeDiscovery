#!/usr/bin/python
#Abdellah Fourtassi 2018
from optparse import OptionParser
import random
import math


#Input1: unsegmented corpus at level N+1
#Input2: segmented corpus for level N

#Goal: segment input1 exactly according to the boundaries in input 2

def main():
    usage = "usage: %prog [options] CORPUS_TEXT"
    parser = OptionParser(usage)
    
    (options, args) = parser.parse_args()
    seg_input=args[0]
    gold=args[1]

    #Extract boundary sequence from gold (segmented corpus) which I am going to use to segment input
    gold_bound_all = [] 
    for line in open(gold):
        bound = [0] #boundary sequence from gold which we are going to use to segment input 
        l = line.split()
	for word in l:
	    b = len(word.split(':')) #number of characters in the word
	    bound.append(bound[len(bound)-1]+b)
        gold_bound_all.append(bound)
	    
    #Now use boundary sequences to segment the input
    count=0
    for line in open(seg_input):
        l=line.split()
        segmentation=[]
	bound=gold_bound_all[count]
        for i in range(len(bound)-1):
            segmentation.append(l[bound[i]:bound[i+1]])
        sent=''
        for i in segmentation:
	    word= ":".join(i)
	    sent=sent+word+' '
	count=count+1
	print sent


if __name__ == "__main__":
    main()


