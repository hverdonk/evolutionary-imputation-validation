NEXUS = ["adh.nex", "bglobin.nex", "camelid.nex", "ENCenv.nex", "flavNS5.nex",
                "HepatitisD.nex", "HIVvif.nex", "IAV_Chen.nex", "lysin.nex",            
                "yokoyama.rh1.cds.mod.1-990.nex"]
# when running tester=MITO_NEXUS, add --code Vertebrate-mtDNA right after the --alignment argument
MITO_NEXUS = ["COXI.mtnex"]


HYPHYMPI="/home/hverdonk/hyphy-develop/HYPHYMPI"
LIBPATH="/home/hverdonk/hyphy-develop/res"

rule all:
	input:
		expand("/home/hverdonk/PREI/task5_realWorldData/Atchley/Atchley-{tester}.PRIME.json", tester=MITO_NEXUS)
	#	 expand("/home/hverdonk/PREI/task5_realWorldData/LCAP/LCAP-{tester}.PRIME.json", tester=MITO_NEXUS)    


rule Atchley:
	input:
 		in_sim = "/home/hverdonk/PREI/task5_realWorldData/empirical-alignments/{tester}"
	output:
		"/home/hverdonk/PREI/task5_realWorldData/Atchley/Atchley-{tester}.PRIME.json"
	shell:
		'''
    	mpirun -np 6 {HYPHYMPI} LIBPATH={LIBPATH} prime --alignment {input.in_sim} --code Vertebrate-mtDNA --impute-states Yes --properties Atchley --output {output}
		'''
		
"""
rule LCAP:
	input:
 		in_sim = "/home/hverdonk/PREI/task5_realWorldData/empirical-alignments/{tester}"
	output:
		"/home/hverdonk/PREI/task5_realWorldData/LCAP/LCAP-{tester}.PRIME.json"
	shell:
		'''
    	mpirun -np 6 {HYPHYMPI} LIBPATH={LIBPATH} prime --alignment {input.in_sim} --code Vertebrate-mtDNA --impute-states Yes --properties LCAP --output {output}
		'''
"""
