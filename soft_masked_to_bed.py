from Bio import SeqIO
import re
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(output_file,"w") as out:
	for seq_record in SeqIO.parse(input_file, "fasta"):
		matches = re.finditer("[a-z]+", str(seq_record.seq))
		for m in matches:
			start,end = m.span()
			out.write("\t".join([seq_record.id,str(start),str(end),"\n"]))

