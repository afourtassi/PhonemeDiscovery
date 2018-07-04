#!/usr/bin/python

#Abdellah Fourtassi 2018
from optparse import OptionParser
import random
import math

def main():
    usage = "usage: %prog [options] CORPUS_TEXT"
    parser = OptionParser(usage)
    
    (options, args) = parser.parse_args()
    AGinput=args[0]

    #Input 1: unsegmented utterances (
    Sup=False
    if len(args)>1:
        gold=args[1]
	#Input 2: the gold standard
	#If the gold is prided, use the number of boundaries in each utterance as the sole information
	#If the gold is not provided then sample a random number of boundaries for each utterance
        Sup=True
        count=[]
        for linegold in open(gold):
            count.append(len(linegold.split())-1)
    compt=0

    for line in open(AGinput):
        compt=compt+1
        l=line.split()
        maxSeg=len(l)
        if Sup==True:
            nbrBound=count[compt-1]
        else:
            nbrW=maxSeg/6.0 - 1
            if nbrW <= 0:
                nbrBound=0
            elif nbrW - math.floor(nbrW)>=0.5:
                nbrBound=int(math.ceil(nbrW))
            elif nbrW - math.floor(nbrW)< 0.5:
                nbrBound=int(math.floor(nbrW))
        segmentation=[]
        if nbrBound != 0:
            bound=random.sample(range(1,maxSeg),nbrBound)
            bound.insert(0,0)
	    bound_sort=sorted(bound)
            for i in range(len(bound)-1):
                segmentation.append(l[bound_sort[i]:bound_sort[i+1]])
            segmentation.append(l[bound_sort[len(bound)-1]:len(l)])
        else:
            segmentation.append(l)
        sent=''
        for i in segmentation:
	    word= ":".join(i)
	    sent=sent+word+' '
	print sent


if __name__ == "__main__":
    main()


