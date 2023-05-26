#!/bin/bash
module load bioinfo/ncbi-blast-2.7.1+
if [ -z $1 ] || [ -z $2 ] || [ -z $3 ]
then
	echo "Usage : bash run_blastn_short.sh database.fasta query.fasta output_name <coverage_filter(int)>"
	exit
fi

if [ -z $4 ]
then
	COV=85   
else 
	COV=$4
fi
makeblastdb -in $1 -dbtype nucl

blastn -task blastn-short -db $1 -query $2 -outfmt "6 qseqid sseqid evalue pident qcovus bitscore stitle" -out "${3}.txt"
cat "${3}.txt" | sort -k5n | awk -v COV=$COV '$5>COV {print}' > "${3}_filtered_cov_${COV}.txt"




