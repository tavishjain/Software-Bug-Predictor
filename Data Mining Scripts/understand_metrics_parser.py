# Understand CMD help URL -> https://scitools.com/support/commandline/

# 1. Run this statement in ubuntu terminal to flatten the directory 
# find . -iname '*.java' -exec cp \{\} ./ \;

# 2. Delete folders
# rm -r */

# 3. Delete all files except .java
# find . -type f ! -name '*.java' -delete

# =====================DIRECTORY CLEANING DONE===========================

# 0. Pre-processing steps
# 	path = <<pwd>>
# Make a shortcut of the und executable on the current location 
# 	ln -s path/scitools/bin/linux64/und .


# 1. Create new project
# 	./und create -languages Java <<name>>.udb

# 2. Add files
# 	./und add path
 
# 3. Set the metrics to be generated to all and specify the path for output csv
#	./und settings –metrics all
# 	./und settings –metricsOutputFile path/metrics.csv

# 4. Set commands for output
# 	./und analyze
# 	./und report
# 	./und metrics

import optparse, sys, os

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

os.system("find . -iname '*.java' -exec cp \{\} ./ \;")
os.system("rm -r */")
os.system("find . -type f ! -name '*.java' -delete")
print("		Directory Cleaning Done !!!")