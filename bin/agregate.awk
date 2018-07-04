BEGIN{
    if (!N)N=1
}
function flush(a){
    gsub("^ +","",a)
    gsub(" +$","",a)
    gsub(" +"," ",a)
    print "<s> " a " </s>"; 
}
{
    if($1=="<s>") $1=""
    if($NF=="</s>") $NF=""
a=a " " $0
nb++
if (nb>=N) {
    flush(a)
    a="";nb=0
  }

}
END{
    if(a)flush(a)
}