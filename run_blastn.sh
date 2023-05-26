#!/bin/bash
module load bioinfo/ncbi-blast-2.7.1+
if [ -z $1 ] || [ -z $2 ] || [ -z $3 ]
then
        echo "Usage : bash run_blastn.sh database.fasta query.fasta output_name <coverage_filter(int)> <gaps_filter(int)>"
        exit
fi

if [ -z $4 ]
then
        COV=70
else
        COV=$4
fi

if [ -z $5 ]
then 
	GAPS=5
else
	GAPS=$5
fi

if ! [[ -f "${1}.nhr" ]]
then
	makeblastdb -in $1 -dbtype nucl
fi

blastn -task blastn -max_target_seqs 1 -db $1 -query $2 -outfmt "6 qseqid sseqid evalue pident qcovus gaps bitscore stitle" -out "${3}.txt"
cat "${3}.txt" | sort -k5n | awk -v COV=$COV -v GAPS=$GAPS '($5>COV && $6<GAPS ) {print}' > "${3}_filtered_cov_${COV}_gaps_${GAPS}.txt"
