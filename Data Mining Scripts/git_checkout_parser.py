import optparse, sys, os, re, time, subprocess
from datetime import datetime
from pathlib import Path
from subprocess import *

def jarWrapper(*args):
    process = Popen(['java', '-jar'] + list(args), stdout=PIPE, stderr=PIPE)
    ret = []
    while process.poll() is None:
        line = process.stdout.readline()
        if line != '' and line.endswith('\n'):
            ret.append(line[:-1])
    stdout, stderr = process.communicate()
    ret += stdout.split('\n')
    if stderr != '':
        ret += stderr.split('\n')
    ret.remove('')
    return ret

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
# 8. Module entropy                    - 
# 9. number of defects in previous     - 
# 10. metrics                     - 

size_diff = list()
actual_size = list()

df = pd.read_excel('whatchanged_data.xlsx')

# os.system('curl -o ckjm.jar https://github.com/mjureczko/CKJM-extended/releases/download/ckjm_ext-2.2/ckjm_ext.jar')


for commit in df['Commit_Hash']:
	# time.sleep(2)
	os.system('git checkout ' + str(commit))
	subprocess.call(['java', '-jar', 'ckjm.jar'])
	# args = ['ckjm.jar'] # Any number of args to be passed to the jar file
	# result = jarWrapper(*args)

	# ans = subprocess.check_output(['java', '-jar', 'ckjm.jar'])
	# print(result)
	# size = subprocess.check_output(['du','-sh', '-k', '.']).split()[0].decode('utf-8')
	# actual_size.append(size)
	# if len(size_diff) == 0:
	# 	size_diff.append(size)
	# else:
	# 	previous_size = int(actual_size[len(actual_size) - 2])
	# 	modified_size = int(size) - previous_size
	# 	size_diff.append(modified_size)

print(len(size_diff), "\n")

for i in range(len(size_diff)):
	print(size_diff[i])