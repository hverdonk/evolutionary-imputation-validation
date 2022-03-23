import argparse
import json
import sys
from collections import Counter
from operator import itemgetter
from Bio import SeqIO
from math import log


arguments = argparse.ArgumentParser(description='Combine analysis results for Omicron selection')
arguments.add_argument('-f',    '--fasta',          help = 'Input FASTA file',   required = False, type = str)
arguments.add_argument('-n',    '--nexus',          help = 'Input Nexus file',  required = False, type = str)
arguments.add_argument('-p',    '--prime',          help = 'PRIME results file', required = True, type = str)
arguments.add_argument('-s',    '--sequence',       help = 'The sequence of interest (case sensitive)', required = True, type = str)

settings = arguments.parse_args()

### read the FASTA file and retrieve codons for the sequence

sequence = None

if settings.fasta:
    with open(settings.fasta) as handle:
        for record in SeqIO.parse(handle, "fasta"):
            if record.id == settings.sequence:
                S = str (record.seq)
                sequence = []
                for i in range (0,len (S),3):
                        sequence.append (S[i:i+3])
                
                break
elif settings.nexus:
    with open(settings.nexus) as handle:
        for record in SeqIO.parse(handle, "nexus"):
            if record.id == settings.sequence:
                S = str (record.seq)
                sequence = []
                for i in range (0,len (S),3):
                        sequence.append (S[i:i+3])
                
                break
            
if not sequence:
    raise (BaseException ("Did not find '%s' in the sequence file" % settings.sequence))
        
        
N = 0        
with open(settings.prime) as handle:
    PRIME = json.load (handle)["MLE"]["Imputed States"]["0"]
    # collect predictions for the requested sequence
    bySite = {}
    for s in PRIME:
        if PRIME [s]:
            bySite [int (s) + 1] = PRIME [s][settings.sequence.upper()]
            N += 1
        else:
            bySite [int (s) + 1] = None # site is invariable
            
# count the number of VARIABLE sites

# print ("Loaded predictions on %d variable sites" % N)

# check to see for how many of those sites the actual state matches the most likely predicted state


MOST_LIKELY_MATCH = 0
MEAN_PROBABILITY  = 0
RATIO_TO_SECOND   = []
IN_SET = 0

# print ("Mismatches at the following sites")
for site in range (len (bySite)):
    predictions = bySite[site+1]
    if predictions:
        sorted_predictions = sorted (predictions.items (), key = itemgetter(1), reverse = True)
        if sorted_predictions[0][0] == sequence[site]:
            MOST_LIKELY_MATCH += 1
            MEAN_PROBABILITY += sorted_predictions[0][1]
            if len (sorted_predictions) > 1:
                RATIO_TO_SECOND.append (log (sorted_predictions[0][1],2) - log (sorted_predictions[1][1],2))
            else: 
                RATIO_TO_SECOND.append (20.)
        else:
            pass
            # print ("Site %4d. ACTUAL = %s, PREDICTED = %s, PR (%s) = %10.8g, PR (%s) = %10.8g" % (site+1, sorted_predictions[0][0], sequence[site], sorted_predictions[0][0], sorted_predictions[0][1], sequence[site], predictions[sequence[site]] if  sequence[site] in predictions else 0.))    
            
        if sequence[site] in predictions:
            IN_SET += 1
        
        
# print ("")
# print ("SEQUENCE state MATCHED MOST LIKELY prediction at %d / %d sites" % (MOST_LIKELY_MATCH, N))
# print ("SEQUENCE state was in the set of predictions at %d / %d sites" % (IN_SET, N))
# print ("Among those, mean predicted probability is %g" % (MEAN_PROBABILITY / N))
# print ("Among those, the mean log odds compared to any the second prediction was %g" % (sum (RATIO_TO_SECOND) / N))
print(N,MOST_LIKELY_MATCH,IN_SET,MEAN_PROBABILITY,sum(RATIO_TO_SECOND),MEAN_PROBABILITY / N)

