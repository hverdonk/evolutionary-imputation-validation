sim500 = ["ladderized-tree-5-00.replicate.%s" % str(i) for i in range(1, 21)]
sim100 = ["ladderized-tree-1-00.replicate.%s" % str(i) for i in range(1, 21)]
sim025 = ["ladderized-tree-0-25.replicate.%s" % str(i) for i in range(1, 21)]
sim001 = ["ladderized-tree-0-01.replicate.%s" % str(i) for i in range(1, 21)]
TESTER = sim500 + sim100 + sim025 + sim001

HYPHYMPI="/home/hverdonk/hyphy-develop/HYPHYMPI"
LIBPATH="/home/hverdonk/hyphy-develop/res"

rule all:
	input:
		expand("/home/hverdonk/PREI/task4_varyBranchLength/LCAP/LCAP-{tester}.PRIME.json", tester=TESTER)

""" 
rule Atchley:
	input:
 		in_sim = "/home/hverdonk/PREI/task4_varyBranchLength/ladderized-tree-sim/{tester}"
	output:
		"/home/hverdonk/PREI/task4_varyBranchLength/Atchley/Atchley-{tester}.PRIME.json"
	shell:
		'''
    	mpirun -np 6 {HYPHYMPI} LIBPATH={LIBPATH} prime --alignment {input.in_sim} --impute-states Yes --properties Atchley --output {output}
		'''
"""

rule LCAP:
	input:
 		in_sim = "/home/hverdonk/PREI/task4_varyBranchLength/ladderized-tree-sim/{tester}"
	output:
		"/home/hverdonk/PREI/task4_varyBranchLength/LCAP/LCAP-{tester}.PRIME.json"
	shell:
		'''
    	mpirun -np 6 {HYPHYMPI} LIBPATH={LIBPATH} prime --alignment {input.in_sim} --impute-states Yes --properties LCAP --output {output}
		'''

