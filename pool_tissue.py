from sys import argv
content = open(argv[1], 'r').read().split('\n')
if len(argv) == 2:
    for i in range(0, len(content), 4):
        if content[i] == '':
            continue
        line_split = content[i].split('_')
        link = '_'.join(line_split[0:6]) + "_rep*_" + '_'.join(line_split[7:])
        print(f'{link}')
else:
    for i in range(0, 28, 4):
        if content[i] == '':
            continue
        line_split = content[i].split('_')
        link = '_'.join(line_split[0:3]) + "_stage*_*_" + "_".join(line_split[5:6]) + "_rep*_" + '_'.join(line_split[7:])
        print(f'{link}')