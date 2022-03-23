
repList = [str(i) for i in list(range(1,21))]
wList = ['0-01','0-25','1-00','5-00']
propList = ['Atchley','LCAP']
animalList = ['HUMAN','CHIMP','BABOON','RHMONKEY','RAT','COW','CAT','HORSE']

with open('run-validate.sh','w') as writeFile:
    writeFile.write('#!/bin/bash\n')
    for animal in animalList:
        for prop in propList:
            for w in wList:
                for rep in repList:
                    writeFile.write('python validatePRIME.py --fasta PREI/task4_varyBranchLength/ladderized-tree-sim/ladderized-tree-'+w+'.replicate.'+rep+' -p PREI/task4_varyBranchLength/'+prop+'/'+prop+'-ladderized-tree-'+w+'.replicate.'+rep+'.PRIME.json -s '+animal+'\n')
