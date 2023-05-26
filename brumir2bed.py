import general_func as gf

import argparse

parser = argparse.ArgumentParser(
                    prog = 'brumir2bed.py',
                    description = 'Get bed file from brumir2ref output, requires the output from brumir2ref and an annotation file generated with blastn, see details in README')

parser.add_argument('-i', '--input', type = str, required = True, help = 'brumir2ref output csv file')
parser.add_argument('-a', '--annotation', type = str, required = False, default=None, help = 'annotation file generated with blastn')
parser.add_argument('-o', '--output', type = str, required = False, help = 'output file')

args = parser.parse_args()
if not args.output:
    args.output = '.'.join(args.input.split('.')[:-1]) + '.bed'

b2ref = gf.brumir2refreader(args.input, annotation_file=args.annotation) if args.annotation != None else gf.brumir2refreader(args.input)
b2ref.to_bed(file_name=args.output)