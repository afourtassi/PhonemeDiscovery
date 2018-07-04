#bdellah Fourtassi 2018
#!/usr/bin/env python
import sys
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

from gensim import corpora, models, similarities, matutils

import random
import numpy
import sys
import os
from pyroc import *

from optparse import OptionParser

from operator import itemgetter

#Function that take all the variables and output the differentiation score 
def run(mycorpus,lang,seg,cont,dim,var,Mydict):

    #dictionary

    dictionary = corpora.Dictionary(line.split() for line in open(mycorpus))

    once_ids = [tokenid for tokenid, docfreq in dictionary.dfs.iteritems() if docfreq==1 ]

    dictionary.filter_tokens(once_ids)

    dictionary.compactify()

    dictionary.save('tmp_'+lang+'_'+cont+'_'+seg+'/form'+lang+'_'+var+'_'+cont+'_'+str(dim)+'.dict')

    dictionary = corpora.Dictionary.load('tmp_'+lang+'_'+cont+'_'+seg+'/form'+lang+'_'+var+'_'+cont+'_'+str(dim)+'.dict')

    id2token = dict((v, k) for k, v in dictionary.token2id.iteritems())

    # Create and serialize the corpus

    corpus = [dictionary.doc2bow(line.split()) for line in open(mycorpus)]

    corpora.MmCorpus.serialize('tmp_'+lang+'_'+cont+'_'+seg+'/form'+lang+'_'+var+'_'+cont+'_'+str(dim)+'.mm', corpus)

    corpus = corpora.MmCorpus('tmp_'+lang+'_'+cont+'_'+seg+'/form'+lang+'_'+var+'_'+cont+'_'+str(dim)+'.mm')

#TF-Idf transform

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

#LSA transform

    lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=dim)

    U = lsi.projection.u
    S = lsi.projection.s
    US=numpy.multiply(U,S)
    
#Create a word-word similarity matrix

    termcorpus=matutils.Dense2Corpus(US.T)

    corpora.MmCorpus.serialize('tmp_'+lang+'_'+cont+'_'+seg+'/termcorpus_form'+lang+'_'+var+'_'+cont+'_'+str(dim)+'.mm', termcorpus)

    termcorpus = corpora.MmCorpus('tmp_'+lang+'_'+cont+'_'+seg+'/termcorpus_form'+lang+'_'+var+'_'+cont+'_'+str(dim)+'.mm')
    
    index=similarities.MatrixSimilarity(termcorpus)

    index.save('tmp_'+lang+'_'+cont+'_'+seg+'/form'+lang+'_'+var+'_'+cont+'_'+str(dim)+'.index')

    index = similarities.MatrixSimilarity.load('tmp_'+lang+'_'+cont+'_'+seg+'/form'+lang+'_'+var+'_'+cont+'_'+str(dim)+'.index')


    lt=list(termcorpus)
    n=len(lt)
   
    myscore=[]
    #for ru in range(100):
    resulta=[]
    result_rand=[]
    
    # For each word (which has more than 1 sub-word), select randomly two sub-words and introduce/compare to two randomly selected sub-words form the lexicon. Repeat this operatin 100 times and take the average 
    for it in range(100):
        data=[]

        for cat in Mydict:
            if len(Mydict[cat])>1:
                l=len(Mydict[cat])
                i=random.randint(0,l-1)
                j=i
                while j == i:
                    j=random.randint(0,l-1)

                tok1=Mydict[cat][i]
                tok2=Mydict[cat][j]
        
                if (tok1 in dictionary.token2id and tok2 in dictionary.token2id):
                    id1=dictionary.token2id[tok1]
                    id2=dictionary.token2id[tok2]
                    p=index[lt[id1]][id2]
                    data.append((1,p))
		   
        #Random pair chosen from dictionary
                
                    k1=random.randint(0,len(id2token)-1)
                    k2=k1
                    while k2==k1:
                        k2=random.randint(0,len(id2token)-1)

                    p_rand=index[lt[k1]][k2]
                    data.append((0,p_rand))

 
        roc=ROCData(data)
        myscore.append(roc.auc())
	

    print  seg +'\t'+lang+ '\t'+var+'\t'+ cont+ '\t'+ str(dim)+ '\t'+ str(numpy.mean(myscore))+'\t'+ str(numpy.std(myscore))


    return                         


#This dictionary takes word at level (i) and match them with finer-versions (cat -> {cath, ca?})
def makeDict(token1,token2):    
    
    toktab_1=[]
    toktab_2=[]

    Mydict={}

    for line in open(token1):
        l=line.split()[0]
        toktab_1.append(l)
    
    for line in open(token2):
        l=line.split()[0]
        toktab_2.append(l)

    for i in range(len(toktab_1)):
        if toktab_1[i] in Mydict:
            if toktab_2[i] not in Mydict[toktab_1[i]]:
                Mydict[toktab_1[i]].append(toktab_2[i])

        else:

            Mydict[toktab_1[i]]=[toktab_2[i]]

    return Mydict
    

def main():
    usage = "usage: %prog [options] CORPUS_TEXT"
    parser = OptionParser(usage)
     
    (options, args) = parser.parse_args()
         
    lang=args[0]
    seg=args[1]
    cont=args[2]

   
    if lang=='Eng':
        levels=["h_2","h_4","h_10", "h_19", "phonemic", "htk_80", "htk_160", "htk_320","htk_640"]
    elif lan=='Jap':
        levels=["h_2","h_4","h_8", "h_13", "phonemic", "htk_50", "htk_100", "htk_200","htk_400"]


    for i in range(len(levels)-1):

        token1='derived_'+lang+'_'+seg+'/'+levels[i]+'_'+lang+'.token'
        token2='derived_'+lang+'_'+seg+'/'+levels[i+1]+'_bis_'+lang+'.token'


        mydict=makeDict(token1,token2)
 		
        
        mycorpus='derived_'+lang+'_'+seg+'/'+levels[i+1]+'_bis_'+lang+'.ag'+cont
        #for dim in [5,10,20,50,100,200,500]:
        for dim in [200]:
            run(mycorpus,lang,seg,cont,dim,levels[i],mydict)  
                
if __name__ == "__main__":
    main()            
