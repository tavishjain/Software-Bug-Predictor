# Understand CMD help URL -> https://scitools.com/support/commandline/

# 1. Run this statement in ubuntu terminal to flatten the directory 
# find . -iname '*.java' -exec cp \{\} ./ \;

# 2. Delete folders
# rm -r */

# 3. Delete all files except .java
# find . -type f ! -name '*.java' -delete

# =====================DIRECTORY CLEANING DONE===========================

# 0. Pre-processing steps
# 	path = <<pwd of home dir>>
# Make a shortcut of the und executable on the current location 
# 	ln -s path/scitools/bin/linux64/und .


# 1. Create new project
# 	./scitools/bin/linux64/und create -db <<name>>.udb -languages Java

# 2. Add files
# 	./scitools/bin/linux64/und add path
 
# 3. Set the metrics to be generated to all and specify the path for output csv
#	./scitools/bin/linux64/und settings –metrics all
# 	./scitools/bin/linux64/und settings –metricsOutputFile path/metrics.csv

# 4. Set commands for output
# 	./scitools/bin/linux64/und analyze
# 	./scitools/bin/linux64/und metrics

# Save stuff in common repo
# ./Dir|
#      |->e parent_dir|
#                    |-> scitools
#                    |-> (Cloned Repo)
# ./scitools/bin/linux64/und
import optparse, sys, os, time

parser  =   optparse.OptionParser()
options, args   =   parser.parse_args()

if len(args):
    path = args.pop(0)
else:
    print ("You must specify a git object as the first argument")
    sys.exit(os.EX_NOINPUT)

parent_dir = os.getcwd() 

repo_location = str(path)
os.chdir(repo_location)
# os.system("cp commands.txt " + repo_location + "/commands.txt")
# os.system("cp " + parent_dir + "/commands.txt commands.txt")

# os.system("find . -iname ('*.java' '*.txt') -exec cp \{\} ./ \;")
# os.system("rm -r */")
# os.system("find . -type f ! -name ('*.java' '*.txt') -delete")

#Cleaning all files and extracting .java files to main folder, deleting all except java and xlsx
os.system("find . -iname '*.java' -exec cp \{\} ./ \;")
os.system("rm -rf */")
os.system("find . -type f ! -name '*.java' -o -name '*.xlsx' -o -name '*.csv' -delete")
# os.system('rm -f !(*.xlsx|*.csv|*.java)')

# os.system("cp " + parent_dir + "/commands.txt commands.txt")
print("\n=> Directory Cleaning Done !!!")

# path_of_und = parent_dir + "/scitools/bin/linux64/und"
path_of_und = parent_dir + "/scitools/bin/pc-win64/und"
# os.system("ln -s " + path_of_und)

print("\n=> Starting metrics generation !!!")

run_commands_txt = path_of_und + " " + parent_dir + "/commands.txt"
# os.system("./scitools/bin/linux64/und commands.txt")
os.system(run_commands_txt)
	
# os.system("./scitools/bin/linux64/und create -db -languages Java " + path + ".udb")
# os.system("./scitools/bin/linux64/und open " + path + ".udb")

# os.system("./scitools/bin/linux64/und add .")
 
# os.system("./scitools/bin/linux64/und settings –metrics all")
# os.system("./scitools/bin/linux64/und settings –metricsOutputFile " + path + "/metrics.csv")

# os.system("./scitools/bin/linux64/und analyze")
# os.system("./scitools/bin/linux64/und metrics")