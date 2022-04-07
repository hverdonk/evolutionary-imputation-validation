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
# arguments.add_argument('-s',    '--sequence',       help = 'The sequence of interest (case sensitive)', required = True, type = str)

settings = arguments.parse_args()

filename = settings.prime.split('/')[-1]
prop = filename.split('-')[0]

### read the alignment file and retrieve codons for the sequence

sequence = None

if settings.fasta:
    alignment = settings.fasta.split('/')[-1]
    branch_seqs = {}
    with open(settings.fasta) as handle:
        for record in SeqIO.parse(handle, "fasta"):
            branch_seqs[record.id] = []
            S = str (record.seq)
            for i in range (0,len (S),3):
                branch_seqs[record.id].append (S[i:i+3])
                
elif settings.nexus:
    alignment = settings.nexus.split('/')[-1]
    branch_seqs = {}
    with open(settings.nexus) as handle:
        for record in SeqIO.parse(handle, "nexus"):
            branch_seqs[record.id] = []
            S = str (record.seq)
            for i in range (0,len (S),3):
                branch_seqs[record.id].append (S[i:i+3])


        
num_sites = {}
branch_lengths = {}
branch_predictions = {}
with open(settings.prime) as handle:
    PRIME = json.load (handle)
    for branch in branch_seqs.keys():
        N = 0
        # collect branch length for the current sequence
        curr_branch_lengths = PRIME['branch attributes']['0'][branch]
        branch_lengths[branch] = {}
        branch_lengths[branch]['MG94XREV'] = curr_branch_lengths['Global MG94xREV']
        branch_lengths[branch]['nucleotide_GTR'] = curr_branch_lengths['Nucleotide GTR']
        
        # collect predictions for the current sequence
        predictions = PRIME["MLE"]["Imputed States"]["0"]
        bySite = {}
        for s in predictions:
            if predictions [s]:
                bySite [int (s) + 1] = predictions[s][branch] # predicted codon at a given site
                N += 1
            else:
                bySite [int (s) + 1] = None # site is invariable
        branch_predictions[branch] = bySite
        num_sites[branch] = N
            
# count the number of VARIABLE sites

# print ("Loaded predictions on %d variable sites" % N)

# check to see for how many of those sites the actual state matches the most likely predicted state
for branch in branch_seqs.keys():
    MOST_LIKELY_MATCH = 0
    MEAN_PROBABILITY  = 0
    RATIO_TO_SECOND   = []
    IN_SET = 0

    # print ("Mismatches at the following sites")
    bySite = branch_predictions[branch]
    sequence = branch_seqs[branch]
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
    print(alignment,\
          prop,\
          branch,\
          branch_lengths[branch]['MG94XREV'],\
          branch_lengths[branch]['nucleotide_GTR'],\
          num_sites[branch],\
          MOST_LIKELY_MATCH,\
          IN_SET,\
          MEAN_PROBABILITY/num_sites[branch],\
          sum(RATIO_TO_SECOND)/num_sites[branch])
        
        
# print ("")
# print ("SEQUENCE state MATCHED MOST LIKELY prediction at %d / %d sites" % (MOST_LIKELY_MATCH, N))
# print ("SEQUENCE state was in the set of predictions at %d / %d sites" % (IN_SET, N))
# print ("Among those, mean predicted probability is %g" % (MEAN_PROBABILITY / N))
# print ("Among those, the mean log odds compared to any the second prediction was %g" % (sum (RATIO_TO_SECOND) / N))

