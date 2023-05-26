#Get Sigificant Candidate (GSC) miRNA from mirdeep2 

import os
import argparse
import sys

parser = argparse.ArgumentParser(
                    prog = 'GSC_mirdeep2.py',
                    description = 'Get significant candidate miRNA from mirdeep2 output, requires the output csv from mirdeep2 and known/novel fasta files')

parser.add_argument('-i', '--input', type = str, required = True, help = 'mirdeep2 output csv file')
parser.add_argument('-k', '--known', type = str, required = False, help = 'known fasta file')
parser.add_argument('-n', '--novel', type = str, required = False, help = 'novel fasta file')
parser.add_argument('-o', '--output_radical', type = str, required = False, help = 'output file')
parser.add_argument('-r', '--remove', default=False, action='store_true', help = 'remove randfold non significant miRNA from fasta files')
parser.add_argument('-s', '--score', type = int, required = False, default=-9999, help = 'score threshold for significant miRNA')
args = parser.parse_args()
date_radical = ''
mirdeep2_folder = ''

if os.path.dirname(args.input) != '':
    input_path = os.path.dirname(args.input) + '/'
else:
    input_path = './'

if args.output_radical == None:
    date_radical = os.path.splitext(os.path.basename(args.input))[0].strip("result_") 
    mirdeep2_folder =  "mirna_results_" + date_radical
    args.output_radical = 'GSC_mirdeep2_' + date_radical + "/"
    if args.score != -9999:
          args.output_radical += "score-" + str(args.score) + "_"
    if args.remove == True: 
        args.output_radical += "randfold-yes_"

if args.known == None and args.novel == None:
    known_auto_path = input_path + \
        '/' + mirdeep2_folder + \
        '/known_mature_' + \
        date_radical + \
        "_score-50_to_na.fa"

    novel_auto_path = input_path + '/' +\
        mirdeep2_folder + \
        '/novel_mature_' + \
        date_radical + \
        "_score-50_to_na.fa"
    
    if os.path.isfile(known_auto_path):
        args.known = known_auto_path
    else:
        exit(f"automatic search for known fasta file failed (file {known_auto_path} does not exist), please provide known fasta file")
    
    if os.path.isfile(novel_auto_path):
        args.novel = novel_auto_path
    else:
        exit(f"automatic search for novel fasta file failed (file {novel_auto_path} does not exist), please provide novel fasta file")

elif args.known != None or args.novel != None:
    raise Exception("Please provide both known and novel fasta files or none to trigger default file search")


mode = ''
cont = False
miRNA_dict = {'novel': [], 'known': []}

def check_mirna(miRNA_id, line_split, mode):
    if len(line_split) == 17:
        if args.remove and args.score != -9999:
            if line_split[8] == "yes" and float(line_split[2].split('+')[0][0:-1]) >= args.score:
                miRNA_dict[mode].append(miRNA_id)
            
        elif args.remove and args.score == -9999:
            if line_split[8] == "yes":
                miRNA_dict[mode].append(miRNA_id)
        elif args.score != -9999 and args.remove == False:
            if float(line_split[2].split('+')[0][0:-1]) >= args.score:
                miRNA_dict[mode].append(miRNA_id)
        else:
            exit('how did you get here? That is not supposed to happen! Maybe you forgot to specify the score threshold or the randfold removal option?') 

    else:
        mode = ''


    
with open(args.input, 'r') as file:
    cnt = 0
    for line in file:

        if cont:
            cont = False
            continue
        elif line.startswith('novel miRNAs predicted by miRDeep2'):
            cont = True
            mode = 'novel'
            continue
        elif line.startswith("mature miRBase miRNAs detected by miRDeep2"):
            cont = True
            mode = 'known'
            continue
        elif mode == "novel":
            line_split = line.split('\t')
            miRNA_id = line_split[0]
            check_mirna(miRNA_id, line_split, mode)
            

        elif mode == "known":
            line_split = line.split('\t')
            miRNA_id = line_split[0]
            check_mirna(miRNA_id, line_split, mode)

known_content = open(args.known, 'r').read().split('\n')
significant_known_body = ''
for line in known_content:
    if line.startswith('>'):
        miRNA_id = line.split(' ')[0].strip('>')
        if miRNA_id in miRNA_dict['known']:
            significant_known_body += line + '\n'
    elif miRNA_id in miRNA_dict['known']:
        significant_known_body += line + '\n'

novel_content = open(args.novel, 'r').read().split('\n')
significant_novel_body = ''
for line in novel_content:
    if line.startswith('>'):
        miRNA_id = line.split(' ')[0].strip('>')
        if miRNA_id in miRNA_dict['novel']:
            significant_novel_body += line + '\n'
    elif miRNA_id in miRNA_dict['novel']:
        significant_novel_body += line + '\n'

if not os.path.exists("/".join(args.output_radical.split('/')[0:-1])):
    os.makedirs("/".join(args.output_radical.split('/')[0:-1]))

with open(args.output_radical + "significant_known_mature.fa", 'w') as file:
    file.write(significant_known_body)

with open(args.output_radical + "significant_novel_mature.fa", 'w') as file:
    file.write(significant_novel_body)









