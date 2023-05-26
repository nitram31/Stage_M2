miRNA_dict = {}
file = open("Python/miRBase_mature_GG.fa", 'r').read().split('\n')

def remove_suffix(mir):
    if mir.endswith('-5p'):
        return mir[:-3].lower()
    elif mir.endswith('-3p'):
        return mir[:-3].lower()
    else:
        return mir.lower()

def prec_to_mature(mir):
    # Not yet needed
    return

def mature_to_prec(mir):
    return remove_suffix(mir)

for line in file:

    if line.startswith('>'):
            miRNA_id = line.split(' ')[0].strip('>')
            if miRNA_id not in miRNA_dict:
                miRNA_dict[miRNA_id]= {'header' : line.strip('\n')}

file = open("Python/annotated_prec_id", 'r').read().split('\n')
body = ""
for line in file:
    if line.startswith('Name'): continue
    miRNA_id = line.strip('\n')
    #print(miRNA_id)
    for el in miRNA_dict:
        #print(remove_suffix(el.lower()), el)
        if miRNA_id == remove_suffix(el.lower()) and el not in body:
            print(f'{el} matches {miRNA_id}' )
            body += el + '\n'
            
    


with open("R/GG_mirdentify_extrapolated_id.txt", 'w') as file:
    file.write(body)


     