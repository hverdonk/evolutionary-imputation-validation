# NEXUS = ["adh.nex", "bglobin.nex", "camelid.nex", "ENCenv.nex", "flavNS5.nex", "HepatitisD.nex", "HIVvif.nex", "IAV_Chen.nex", "lysin.nex", "yokoyama.rh1.cds.mod.1-990.nex", "COXI.mtnex"]
                
NEXUS = ["COXI.mtnex"]

HYPHYMPI="/home/hverdonk/hyphy-develop/HYPHYMPI"
LIBPATH="/home/hverdonk/hyphy-develop/res"

rule all:
	input:
		expand("/home/hverdonk/PREI/task5_realWorldData/Atchley/Atchley-{tester}.PRIME.json", tester=NEXUS) + expand("/home/hverdonk/PREI/task5_realWorldData/LCAP/LCAP-{tester}.PRIME.json", tester=NEXUS)    

rule Atchley:
	input:
 		in_sim = "/home/hverdonk/PREI/task5_realWorldData/empirical-alignments/{tester}"
	output:
		"/home/hverdonk/PREI/task5_realWorldData/Atchley/Atchley-{tester}.PRIME.json"
	params:
	        var= lambda wildcards: "Vertebrate-mtDNA" if wildcards.tester == "COXI.mtnex" else "Universal"
	shell:
		'''
    	mpirun -np 6 {HYPHYMPI} LIBPATH={LIBPATH} prime --alignment {input.in_sim} --code {params.var:q} --impute-states Yes --properties Atchley --output {output}
		'''
		
		
rule LCAP:
	input:
 		in_sim = "/home/hverdonk/PREI/task5_realWorldData/empirical-alignments/{tester}"
	output:
		"/home/hverdonk/PREI/task5_realWorldData/LCAP/LCAP-{tester}.PRIME.json"
	params:
	        var= lambda wildcards: "Vertebrate-mtDNA" if wildcards.tester == "COXI.mtnex" else "Universal"
	shell:
		'''
    	mpirun -np 6 {HYPHYMPI} LIBPATH={LIBPATH} prime --alignment {input.in_sim} --code {params.var:q} --impute-states Yes --properties LCAP --output {output}
		'''

