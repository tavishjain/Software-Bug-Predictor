import optparse, sys, os, re, time, subprocess
from datetime import datetime
from pathlib import Path
from subprocess import *

try:
    import git
    import xlrd
    import pandas as pd
except ImportError:
    os.system("apt install python3-pip")
    os.system("pip3 install gitpython")
    os.system("pip3 install pandas")
    os.system("pip3 install xlrd")
    import git 
    import xlrd
    import pandas as pd

parser  =   optparse.OptionParser()

options, args   =   parser.parse_args()

if len(args):
    path = args.pop(0)
else:
    print ("You must specify a git object as the first argument")
    sys.exit(os.EX_NOINPUT)

repo_location = str(path)
os.chdir(repo_location)

g = git.Git(os.getcwd())

# INPUT FEATURES
# 1. Number of File changes            - in git_whatchanged_parser.py and dataframe
# 2. Number of LOC changes             - in git_whatchanged_parser.py and dataframe
# 3. Developer info                    - in git_whatchanged_parser.py and dataframe
# 4. Number of Distinct Contributors   - in git_whatchanged_parser.py and dataframe
# 5. commit message                    - in git_whatchanged_parser.py and dataframe
# 6. Commit time difference            - in git_whatchanged_parser.py and dataframe
# 7. Size of modification              - done - in size_diff
# 8. metrics                     - 

size_diff = list()
actual_size = list()

df = pd.read_excel('whatchanged_data.xlsx')

for commit in df['Commit_Hash']:
    # print('Covering Commit #', commit)
    size = subprocess.check_output(['du','-sh', '-k', '.']).split()[0].decode('utf-8')
    actual_size.append(size)
    if len(size_diff) == 0:
        size_diff.append(size)
    else:
        previous_size = int(actual_size[len(actual_size) - 2])
        modified_size = int(size) - previous_size
        size_diff.append(modified_size)

print("Size of modification: ", len(size_diff), "\n")

# for i in range(len(size_diff)):
	# print(size_diff[i])