for i in test3_* ;
do cp "$i" data/exp1_"${i/test3_N2_recN/N2_neggame}";
done
