import json

outFile = 'empirical-results.json'

toBeWritten = []
header = True
with open('run-validate.sh','r') as myFile:
    for l in myFile:
        if header:
            header = False
        else:
            tempDict = {'alignment':'',\
                        'taxon':'',\
                        'property':'',\
                        'animal_property':'',\
                        'N':0,\
                        'MOST_LIKELY_MATCH':0,\
                        'IN_SET':0,\
                        'SUM_MEAN_PROBABILITY':0,\
                        'SUM_RATIO_TO_SECOND':0,\
                        'MEAN_PROBABILITY':0
}
            line = l.rstrip().split(' ')
            tempDict['alignment'] = line[3].split('/')[3]
            tempDict['property'] = line[5].split('/')[2]
            tempDict['taxon'] = line[-1]
            tempDict['taxon_property'] = ';'.join([tempDict['taxon'],tempDict['property']])
            toBeWritten.append(tempDict)


index = 0
with open('vout-empirircal.txt','r') as myFile:
    for l in myFile:
        line = [float(i) for i in l.rstrip().split(' ')]
        toBeWritten[index]['N'] = line[0]
        toBeWritten[index]['MOST_LIKELY_MATCH'] = line[1]
        toBeWritten[index]['IN_SET'] = line[2]
        toBeWritten[index]['SUM_MEAN_PROBABILITY'] = line[3]
        toBeWritten[index]['SUM_RATIO_TO_SECOND'] = line[4]
        toBeWritten[index]['MEAN_PROBABILITY'] = line[5]
        # toBeWritten[index]['NOT_PREDICTED'] = line[6]
        index += 1
        
with open(outFile, 'w') as writeFile:
    json.dump(toBeWritten, writeFile, indent=4)

