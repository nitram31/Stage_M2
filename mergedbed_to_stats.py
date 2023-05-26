import general_func as gf
from sys import argv
#path = 'Python/bedfolder/SS_all_novel_sorted_merged.bed'
#path = 'Python/bedfolder/SS_all_known_novel_ok_sorted_merged.bed'
path = argv[1]
print(path)
bed_dict = gf.bedreader(path=path).get_dict()

print(len(list(bed_dict.keys())))
cnt_dict = {}
type = ['Brumir2ref', 'mirdentify', 'mirdeep2']
cat = ['known', 'novel', 'known_novel', 'novel_known']
length_list = []
cnt_list = []
source_list = []

for el in bed_dict:
    tmp_list = []
    id_list = el.split(',')
    start, end = int(bed_dict[el]['start']), int(bed_dict[el]['end'])
    length = end - start
    length_list.append(str(length))
    cnt_list.append(str(len(id_list)))
    #if len(id_list) < 2: continue

    outstr = ""
    source_outstr = ""
    cat_str = ""
    outlist = []
    anot_list = []

    source_outlist = []
    for id in id_list:
        source = id.split('_')[0]
        category = id.split('_')[2]
        #annot = id.split('_')[3] if source != 'mirdentify' else id.split('_')[3][0:id.split('_')[3].index('M')]
        #if annot not in anot_list: anot_list.append(annot)
        if source not in tmp_list: tmp_list.append(source)
        if category not in cat_str and category in cat: 
            cat_str += category if cat_str == "" else '_' + category
            pass
        if source not in type: 
            print("********************************",id) 
            continue
        elif source not in source_outlist:
            source_outlist.append(source)
            pass
    if len(anot_list) > 1: print('**************', anot_list, start, end)
    source_list.append('_'.join(sorted(tmp_list)))
    source_outstr = '_'.join(sorted(source_outlist))

    if source_outstr not in cnt_dict: cnt_dict[source_outstr] = 1
    else: cnt_dict[source_outstr] += 1
    #print(source_list[])
    if cat_str == '':
        continue
    """if cat_str not in cnt_dict: 
        #print(cnt_dict.keys())
        cnt_dict[cat_str] = 1
    else:
        
        cnt_dict[cat_str] += 1"""

print()
print(cnt_dict)
Brumir2ref=cnt_dict['Brumir2ref']
mirdentify=cnt_dict['mirdentify']
mirdeep2=cnt_dict['mirdeep2']
mirdeep2_mirdentify=cnt_dict['mirdeep2_mirdentify']
Brumir2ref_mirdentify=cnt_dict['Brumir2ref_mirdentify'] if 'Brumir2ref_mirdentify' in cnt_dict else 0
Brumir2ref_mirdeep2=cnt_dict['Brumir2ref_mirdeep2']
Brumir2ref_mirdeep2_mirdentify=cnt_dict['Brumir2ref_mirdeep2_mirdentify'] if 'Brumir2ref_mirdeep2_mirdentify' in cnt_dict else 0
print(f"""Brumir2ref= {Brumir2ref}
mirdentify = {mirdentify} 
mirdeep2= {mirdeep2} 
mirdeep2_mirdentify = {mirdeep2_mirdentify}
Brumir2ref_mirdentify = {Brumir2ref_mirdentify}
Brumir2ref_mirdeep2 = {Brumir2ref_mirdeep2}
Brumir2ref_mirdeep2_mirdentify = {Brumir2ref_mirdeep2_mirdentify}""")
"""Brumir2ref= 6415 
mirdentify = 26 
mirdeep2= 468 
mirdeep2_mirdentify = 117
Brumir2ref_mirdentify = 8
Brumir2ref_mirdeep2 = 83
Brumir2ref_mirdeep2_mirdentify = 119"""
#print(','.join([str(i) for i in list(el)]))
#gf.write_file('R/SS_stats_len.txt', '\n'.join(length_list))
#gf.write_file('R/SS_stats_cnt.txt', '\n'.join(cnt_list))
#gf.write_file('R/GG_length_source.txt', '\n'.join([','.join([str(i) for i in list(el)]) for el in zip(length_list, source_list)]))
