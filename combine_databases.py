miRNA_dict = {}
with open("Python/mirgendb_all.tsv", "r") as file:
    
    for line in file:
        line_split = line.split('\t')
        
        miRNA_id = line_split[0]
        if line_split[1] == 'None':
            miRNA_dict[miRNA_id] = {'seq': '', 'header': ''}

body = ''

file = open("Python/mirgenedb_ALL_mature.fa", 'r').read().split('\n')

for line in file:
    
    print(line)
    if line.startswith('>'):
            
            miRNA_id = line.split(' ')[0].strip('>').split("_")[0]
            print(miRNA_id)
            if miRNA_id in miRNA_dict:
                miRNA_dict[miRNA_id]['header'] = line.strip('\n')
                write = True
            else:
                write = False
    elif write:
        miRNA_dict[miRNA_id]['seq'] = line.strip('\n')

for el in miRNA_dict:
    if miRNA_dict[el]['seq'] != '':
        body += miRNA_dict[el]['header'] + '\n' + miRNA_dict[el]['seq'] + '\n'

with open("Python/all_mirgenedb_exclusive_mirna", 'w') as file:
    file.write(body)