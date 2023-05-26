#!/bin/bash

if [[ -z $1 || -z $2 ]]
then
      echo "Usage: bash run_brumir2ref_para.sh <brumir_output.fa> <genome.fa> <int (optional): number of parallel executions> <str (optional): prefix>
Note that prefix must be used if this scripted is used in parallel, like launched via sarray
Unused option should be replaced by \"none\". Ex: bash run_brumir2ref_para.sh brumir_output.fa genome.fa none none "
	exit
fi

if [ -z $3 ] || [ "$3" == "none" ]
then
      num_files=7
else
      num_files=$3
fi

if [ -z $4 ] || [ "$4" = "none" ]
then
      PREFIX=""
else
      PREFIX="_$4"
fi

total_lines=$(wc -l < $1)

((lines_per_file = (total_lines + num_files - 1) / num_files))

if ! [ $(( $lines_per_file  % 2)) -eq 0 ] 
then 
	lines_per_file=$((lines_per_file+1)) 
fi
# Split the actual file, maintaining lines.

mkdir .tmp/
mkdir .tmp/temp_res$PREFIX
mkdir logs
touch .tmp/brumir_rf_para${PREFIX}.txt

OUTDIR=".tmp/temp_res${PREFIX}/"
CMDFILE=".tmp/brumir2ref_para${PREFIX}.txt"

split --lines=${lines_per_file} $1 .tmp/temp_res${PREFIX}/file_split.

for file in $(ls .tmp/temp_res${PREFIX}/file_split.*)
do
echo "/usr/bin/perl /home/mracoupeau/work/softwares/BrumiR/brumir2reference.pl -a $file -b $2 -t 1 -p ${OUTDIR}filesplit_${file##*.}" >> $CMDFILE
done

J_id=$(srun sarray -J brumir2ref_split -o logs/%j.out -e logs/%j.err --%=$num_files --mem=8G $CMDFILE | tr ' ' '\t' | cut -f4)
sleep 30

END=0
CNT=0
while [ "$END" -eq 0 ] 
do
	CNT=0
	for job_number in $(seq $num_files)
	do
		echo $J_id"_"$job_number
		state=$( seff $J_id"_"$job_number | grep -Eo "State: .* \(")
		COMP="COMPLETED"
		if [[ "$state" == *"$COMP"* ]]
		then
			echo $J_id"_"$job_number" completed"
			CNT=$((CNT+1))
		fi
	done
	if [[ "$CNT" -eq "$num_files" ]]
	then
		END=1
	else
		#echo "not yet"
		sleep 60
	fi
done
mkdir "brumir2ref"
JOINFILE="brumir2ref/final_b2ref_file.passfilter${PREFIX}.txt" 
for outfile in $(ls "${OUTDIR}"*".passfilter.txt")
do
	if [ -f $JOINFILE ]
	then
      		$(tail -n+2 $outfile >> $JOINFILE)
	else
      		$(cat $outfile > $JOINFILE)	
	fi
done

rm .tmp/file_split.*
rm -r $OUTDIR
rm $CMDFILE
