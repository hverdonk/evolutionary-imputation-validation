import subprocess, os, sys, time

alignment_dir="/home/hverdonk/PREI/task2_varyOmega/"
output_dir="/home/hverdonk/PREI/task3_varyProperties"

HYPHYMPI='/home/hverdonk/hyphy-develop/HYPHYMPI'
LIBPATH="/home/hverdonk/hyphy-develop/res"
PRIME="/home/hverdonk/hyphy-develop/res/TemplateBatchFiles/SelectionAnalyses/PRIME.bf"

alignments=[i for i in os.listdir(alignment_dir) if i.find('replicate')!=-1]

# Run Atchley
# for align in alignments:
#     Atchley_job=align+".Atchley"
#     Atchley_output=output_dir+"/Atchley/"+Atchley_job+'.PRIME.json'
    
#     input_string = " ".join([str(i) for i in [HYPHYMPI,"LIBPATH="+LIBPATH,PRIME,"--alignment",alignment_dir+align,"--impute-states", "Yes","--properties","Atchley","--output",Atchley_output]])

    # qsub
#     subprocess.run(["qsub","-q", "epyc2", "-V", "-l", "walltime=999:00:00", "-l", "nodes=1:ppn=16", "-N", Atchley_job], input = (input_string), universal_newlines = True)
#     print(Atchley_job, Atchley_output)

# Run LCAP   
for align in alignments:
    LCAP_job=align+".LCAP"
    LCAP_output=output_dir+"/LCAP/"+LCAP_job+'.PRIME.json' 

    input_string = " ".join([str(i) for i in [HYPHYMPI,"LIBPATH="+LIBPATH,PRIME,"--alignment",alignment_dir+align,"--impute-states", "Yes","--properties","LCAP","--output",LCAP_output]])

    # qsub
    subprocess.run(["qsub","-q", "epyc2", "-V", "-l", "walltime=999:00:00", "-l", "nodes=1:ppn=16", "-N", LCAP_job], input = (input_string), universal_newlines = True)
    print(LCAP_job, LCAP_output)
    time.sleep(1)
