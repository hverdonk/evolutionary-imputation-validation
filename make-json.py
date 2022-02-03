import json

outFile = 'simple.json'

toBeWritten = []
header = True
with open('run-validate.sh','r') as myFile:
    for l in myFile:
        if header:
            header = False
        else:
            tempDict = {'animal':'',\
                        'property':'',\
                        'omega':'',\
                        'all_three':'',\
                        'rep':0,\
                        'N':0,\
                        'MOST_LIKELY_MATCH':0,\
                        'IN_SET':0,\
                        'SUM_MEAN_PROBABILITY':0,\
                        'SUM_RATIO_TO_SECOND':0,\
                        'MEAN_PROBABILITY':0}
            line = l.rstrip().split(' ')
            tempDict['property'] = line[5].split('/')[2]
            tempDict['rep'] = int(line[3].split('.')[-1])
            tempDict['omega'] = float(line[3].split('ladderized-tree-')[-1].split('.replicate')[0].replace('-','.'))
            tempDict['animal'] = line[-1]
            tempDict['all_three'] = ';'.join([tempDict['animal'],tempDict['property'],str(tempDict['omega'])])
            toBeWritten.append(tempDict)

index = 0
with open('vout.txt','r') as myFile:
    for l in myFile:
        line = [float(i) for i in l.rstrip().split(' ')]
        toBeWritten[index]['N'] = line[0]
        toBeWritten[index]['MOST_LIKELY_MATCH'] = line[1]
        toBeWritten[index]['IN_SET'] = line[2]
        toBeWritten[index]['SUM_MEAN_PROBABILITY'] = line[3]
        toBeWritten[index]['SUM_RATIO_TO_SECOND'] = line[4]
        toBeWritten[index]['MEAN_PROBABILITY'] = line[5]
        index += 1

with open(outFile, 'w') as writeFile:
    json.dump(toBeWritten, writeFile, indent=4)
