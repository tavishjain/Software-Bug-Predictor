import optparse, sys, os, re, time, subprocess
from datetime import datetime
from pathlib import Path
from subprocess import *

def cartesian_product(left, right):
	return pd.concat([pd.concat([left]*len(right)).sort_index().reset_index(drop=True),
       pd.concat([right]*len(left)).reset_index(drop=True) ], 1)

try:
    import git
    import xlrd
    import numpy as np
    import pandas as pd
except ImportError:
    os.system("apt install python3-pip")
    os.system("pip3 install gitpython")
    os.system("pip3 install pandas")
    os.system("pip3 install numpy")
    os.system("pip3 install xlrd")
    import git 
    import numpy as np
    import xlrd
    import pandas as pd

parser  =   optparse.OptionParser()

options, args   =   parser.parse_args()

if len(args):
    path = args.pop(0)
else:
    print ("You must specify a git object as the first argument")
    sys.exit(os.EX_NOINPUT)

parent_directory = os.getcwd()
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

for i in range(len(df['Commit_Hash'])):
	if i == 0:
		continue
	commit = df['Commit_Hash'][i]
	os.system('git checkout ' + commit)
	print('Covering Commit #', commit)
	# time.sleep(30)
	all_commits_left = df.loc[df['Commit_Hash'] == commit]

	# Run Sub-script
	os.chdir(parent_directory)	
	os.system("python3 understand_metrics_parser.py " + repo_location)

	# Changing directory updates file structure, otherwise it'll give FileNotFoundError
	os.chdir(parent_directory)	
	os.chdir(repo_location)

	#Create dataframe and continue
	new_file_name_metrics = 'metrics' + commit + '.csv'	
	os.rename('metrics.csv', new_file_name_metrics)
	metrics_df_right = pd.read_csv(new_file_name_metrics)
	metrics_df_right = metrics_df_right.loc[metrics_df_right['Kind'] == 'File']
	metrics_df_right.to_csv(new_file_name_metrics)

	os.system("find . -type f ! -name '*.csv' -o -name '*.xlsx' -delete")
	
	os.chdir(parent_directory)	
	os.chdir(repo_location)
	#Add to final_data.csv
	temp_df = cartesian_product(all_commits_left, metrics_df_right)
	req_cols_temp_df = [col for col in temp_df.columns if col.lower()[:7] != 'unnamed']
	temp_df = temp_df[req_cols_temp_df]
	# temp_df = temp_df.drop('Unnamed: 0', axis = 1)
	print(temp_df.info())
	temp_df.to_excel(str(i) + '.xlsx')
	# print(temp_df)
	if os.path.isfile('final_data.xlsx'):
		final_data = pd.read_excel('final_data.xlsx')

		req_cols_final_data = [col for col in final_data.columns if col.lower()[:7] != 'unnamed']
		final_data = final_data[req_cols_final_data]
		print('Final Data: ', final_data.shape)
		final_data = final_data.append(temp_df)
		print('Final Data: ', final_data.shape)
		print('Temp DF: ', temp_df.shape)
		time.sleep(10)
		final_data.to_excel('final_data.xlsx')
	else:
		print('Generating First File.......')
		final_data = temp_df

		req_cols_final_data = [col for col in final_data.columns if col.lower()[:7] != 'unnamed']
		final_data = final_data[req_cols_final_data]
		print('Final Data: ', final_data.shape)
		print('Temp DF: ', temp_df.shape)
		time.sleep(10)
		final_data.to_excel('final_data.xlsx')
