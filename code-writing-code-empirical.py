import os
import glob
from Bio import SeqIO

propList = ['Atchley','LCAP']

with open('run-validate.sh','w') as writeFile:
    writeFile.write('#!/bin/bash\n')
    for prop in propList:
        for filename in glob.glob("PREI/task5_realWorldData/empirical-alignments/*"):
            # get all taxa using biopython
            with open(filename) as handle:
                for record in SeqIO.parse(handle, "nexus"):
                    alignment = filename.split('/')[3]
                    writeFile.write('python3 validatePRIME-empirical.py --nexus '+filename+' -p PREI/task5_realWorldData/'+prop+'/'+prop+'-'+alignment+'.PRIME.json -s '+record.id+'\n')

