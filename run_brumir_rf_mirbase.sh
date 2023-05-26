#!/bin/bash
#SBATCH -J BrumiR_rf_chicken_liver
#SBATCH -p workq 
#SBATCH --cpus-per-task=8
export R_LIBS="~/work/Lib"
module load system/R-4.1.2_gcc-9.3.0

/usr/bin/perl /home/mracoupeau/work/softwares/BrumiR/brumir-rf/classify_brumir_with_RF.pl -i $1 -d /home/mracoupeau/work/softwares/BrumiR/brumir-rf/miRbase.mature.animals.fa  -m /home/mracoupeau/work/softwares/BrumiR/brumir-rf/miRbase_animals_rf_model_v02.rds -s $2
