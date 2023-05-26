import general_func as gf

import argparse

parser = argparse.ArgumentParser(
                    prog = 'get_mirdeep_precursor.py',
                    description = 'Get precursor sequence from mirdeep2 output, requires the output csv from mirdeep2')

parser.add_argument('-i', '--input', type = str, required = True, help = 'mirdeep2 output csv file')
parser.add_argument('-o', '--output', type = str, required = False, help = 'output file')

args = parser.parse_args()
if not args.output:
    args.output = '.'.join(args.input.split('.')[:-1]) + '_precursor_list.txt'

mirdeep_dict = gf.mirdeepreader(args.input).get_dict()
#mirbase = gf.fastareader('Python/miRBase_precursor_GG.fa').get_dict()

#prec_list = [i for i in mirbase]

mature_list = [mirdeep_dict['known'][mirna]["mature miRBase miRNA"].split('_')[0] for mirna in mirdeep_dict['known']]
precursor_list = gf.mature_to_precursor(mature_list)
body = ""
for prec in precursor_list: body += prec.split(';')[0] + '\n'

gf.write_file(args.output, body)

