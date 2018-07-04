#Abdellah Fourtassi 2018
#!/bin/bash


#lang can be "Eng" or "Jap"
#seg can be "gold", "seg" or "rand"
lang="$1"
seg="$2"

#Create a temporary file for derived data
derived=derived_"$lang"_"$seg"
if [ ! -d "$derived" ] ; then
mkdir "$derived"
fi

#For each level of granularity i, compute the differentiation score using the next level i+1
if [ "$lang" == Eng ] ; then
declare -a levels=("h_2" "h_4" "h_10" "h_19" "phonemic" "htk_80" "htk_160" "htk_320" "htk_640")

elif [ "$lang" == Jap ]; then
declare -a levels=("h_2" "h_4" "h_8" "h_13" "phonemic" "htk_50" "htk_100" "htk_200" "htk_400")

fi


for i in {0..7}

do 
        level0=${levels[$i]}
	level1=${levels[$i+1]}
	
	#Take gold of i+1 and generate segmentaton input (unsegmented utterances)
	python bin/input2seg.py corpus/corpus_gold/"$level1"."$lang" > "$derived"/"$level1"_"$lang".input 

	#Segmented corpus at level i+1 according to segmentation level i (we need exact matching to identify phoneticaly fine-grained versions of a given words)

        python bin/segment_levels.py "$derived"/"$level1"_"$lang".input corpus/corpus_"$seg"/"$level0"."$lang" > "$derived"/"$level1"_"$lang"."$seg"

	corpus0=corpus/corpus_"$seg"/"$level0"."$lang"
        cat "$corpus0" | gsed 's/ $//g' | gsed 's/ /\n/g' > "$derived"/"$level0"_"$lang".token
 
        corpus1="$derived"/"$level1"_"$lang"."$seg"
        cat "$corpus1" | gsed 's/ $//g' | gsed 's/ /\n/g' > "$derived"/"$level1"_bis_"$lang".token
	
	#Aggregate with different "context" sizes
        awk -f bin/agregate.awk -v N=5 "$corpus1" > "$derived"/"$level1"_bis_"$lang".ag5
        awk -f bin/agregate.awk -v N=10 "$corpus1" > "$derived"/"$level1"_bis_"$lang".ag10
        awk -f bin/agregate.awk -v N=20 "$corpus1" > "$derived"/"$level1"_bis_"$lang".ag20
        awk -f bin/agregate.awk -v N=50 "$corpus1" > "$derived"/"$level1"_bis_"$lang".ag50
        awk -f bin/agregate.awk -v N=100 "$corpus1" > "$derived"/"$level1"_bis_"$lang".ag100
        awk -f bin/agregate.awk -v N=200 "$corpus1" > "$derived"/"$level1"_bis_"$lang".ag200
        awk -f bin/agregate.awk -v N=500 "$corpus1" > "$derived"/"$level1"_bis_"$lang".ag500
 
done

#Create the file to write the summary results
res=res/results_"$seg"_"$lang".txt

# The summary results depend on:
# segmentatin (gold, unsupervised or random)
# language (English or Japanese)
# degree of variation (i.e., granularity)
# context size 
# dimension of the reduced semantic space
# Area Under the Curve (AUC) of the signal distribution (similarity of sub-words pairs: cos(cath, ca?))  vs. noise distribution (similarity of random sub-words, e.g., cosine(food, ca?))  
echo "Segmentation      language        variation       context   dimension       AUC   StD" > "$res"


#for cont in 5 10 20 50 100 200 500
for cont in 20
do

        tmp=tmp_"$lang"_"$cont"_"$seg"  

        if [ ! -d "$tmp" ] ; then
        mkdir "$tmp"
        fi

        python bin/SC.py "$lang" "$seg" "$cont" >> "$res"

        rm -r "$tmp"

done

rm -r "$derived"
