import general_func as gf

import argparse

parser = argparse.ArgumentParser(
                    prog = 'mirdeep2bed.py',
                    description = 'Get bed file from mirdeep2 output, requires the output from mirdeep2.')

parser.add_argument('-i', '--input', type = str, required = True, help = 'mirdeep2 output csv file')

parser.add_argument('-t', '--type', type = str, required = False, help = 'type of the output file, default is known and novel combined, can be either "known" or "novel"')

parser.add_argument('-o', '--output', type = str, required = False, help = 'output file')

args = parser.parse_args()
if not args.output:
    args.output = '.'.join(args.input.split('.')[:-1]) + '.bed'

mirdeep = gf.mirdeepreader(args.input) 
mirdeep.to_bed(file_name=args.output) if args.type == None else mirdeep.to_bed(file_name=args.output, file_type=args.type)