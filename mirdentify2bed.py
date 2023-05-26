import general_func as gf

import argparse

parser = argparse.ArgumentParser(
                    prog = 'mirdentify2bed.py',
                    description = 'Get bed file from mirdentify output, requires the output from mirdeep2.')

parser.add_argument('-k', '--known', type = str, required = False, help = 'mirdentify known output csv file')
parser.add_argument('-n', '--novel', type = str, required = False, help = 'mirdentify novel output csv file')
parser.add_argument('-o', '--output', type = str, required = False, help = 'output file')

args = parser.parse_args()
if not args.output:
    args.output = '.'.join(args.input.split('.')[:-1]) + '.bed'
if not args.known and not args.novel:
    exit('Error: no input file specified, please specify at least one input file (novel or known)')
if not args.known:
    file_type = 'novel'
    mirdentify = gf.mirdentifyreader(novel=args.novel)

elif not args.novel:
    file_type = 'known'
    mirdentify = gf.mirdentifyreader(known=args.known)
else:
    mirdentify = gf.mirdentifyreader(known=args.known, novel=args.novel)


mirdentify.to_bed(file_name=args.output) if args.known and args.novel else mirdentify.to_bed(file_name=args.output, file_type=file_type) 