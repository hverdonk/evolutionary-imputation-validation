import subprocess, os, sys

output_dir="/home/hverdonk/PREI/task2_varyOmega/simple-sim"

job_name="second-task-PREI"
HYPHY='home/hverdonk/hyphy-develop/HYPHYMP'
LIBPATH="/home/hverdonk/hyphy-develop/res"
SIM_MG94="/home/hverdonk/hyphy-analyses/SimulateMG94/SimulateMG94.bf"

# input_string = 'home/hverdonk/hyphy-develop/hyphy /home/hverdonk/hyphy-analyses/SimulateMG94/SimulateMG94.bf --tree tree.nwk --output simple-sim --replicates 5 --omega 5'

input_string = " ".join([str(i) for i in [HYPHY,"LIBPATH="+LIBPATH,SIM_MG94,"--tree tree.nwk --output",output_dir+'simple-sim-5-00',"--replicates 20 --omega 5"]])
# output=output_dir+job_name+'.PRIME.json'


# submit job to qsub scheduler
subprocess.run(["qsub","-q", "epyc2", "-V", "-l", "walltime=999:00:00", "-l", "nodes=1:ppn=1", "-N", job_name, "-o", output_dir], input = (input_string), universal_newlines = True)

print(input_string)
# print(job_name, output)
