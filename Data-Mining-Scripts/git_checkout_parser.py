import optparse, sys, os, re, time, subprocess
from datetime import datetime
from pathlib import Path
from subprocess import *

def cartesian_product(left, right):
	if right.empty == True:
		right = pd.DataFrame(columns = ['Name', 'AvgCyclomatic', 'AvgCyclomaticModified', 'AvgCyclomaticStrict', 'AvgEssential', 'AvgLine', 'AvgLineBlank', 'AvgLineCode', 'AvgLineComment', 'CountDeclClass', 'CountDeclClassMethod', 'CountDeclClassVariable', 'CountDeclExecutableUnit', 'CountDeclFunction', 'CountDeclInstanceMethod', 'CountDeclInstanceVariable', 'CountDeclMethod', 'CountDeclMethodDefault', 'CountDeclMethodPrivate', 'CountDeclMethodProtected', 'CountDeclMethodPublic', 'CountLine', 'CountLineBlank', 'CountLineCode', 'CountLineCodeDecl', 'CountLineCodeExe', 'CountLineComment', 'CountSemicolon', 'CountStmt', 'CountStmtDecl', 'CountStmtExe', 'MaxCyclomatic', 'MaxCyclomaticModified', 'MaxCyclomaticStrict', 'MaxEssential', 'MaxNesting', 'RatioCommentToCode', 'SumCyclomatic', 'SumCyclomaticModified', 'SumCyclomaticStrict', 'SumEssential'])
		right = right.append(pd.Series(0, index = right.columns), ignore_index=True)
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

df = pd.read_excel('whatchanged_data.xlsx')
final_data = pd.DataFrame(columns=['Commit_Hash', 'Author', 'Date_Time', 'Commit_Message', 'Files_Changed', 'Insertions', 'Deletions', 'Bug_present', 'Commit_Time_Diff', 'Name', 'AvgCyclomatic', 'AvgCyclomaticModified', 'AvgCyclomaticStrict', 'AvgEssential', 'AvgLine', 'AvgLineBlank', 'AvgLineCode', 'AvgLineComment', 'CountDeclClass', 'CountDeclClassMethod', 'CountDeclClassVariable', 'CountDeclExecutableUnit', 'CountDeclFunction', 'CountDeclInstanceMethod', 'CountDeclInstanceVariable', 'CountDeclMethod', 'CountDeclMethodDefault', 'CountDeclMethodPrivate', 'CountDeclMethodProtected', 'CountDeclMethodPublic', 'CountLine', 'CountLineBlank', 'CountLineCode', 'CountLineCodeDecl', 'CountLineCodeExe', 'CountLineComment', 'CountSemicolon', 'CountStmt', 'CountStmtDecl', 'CountStmtExe', 'MaxCyclomatic', 'MaxCyclomaticModified', 'MaxCyclomaticStrict', 'MaxEssential', 'MaxNesting', 'RatioCommentToCode', 'SumCyclomatic', 'SumCyclomaticModified', 'SumCyclomaticStrict', 'SumEssential', 'is_changed'])

results_dir = parent_directory + "/results"
if os.path.isdir(results_dir) != True:
	os.mkdir(results_dir)
# writer = pd.ExcelWriter(results_dir)
xlsx_file_name = path.split('/')[-1] + '_data.xlsx'
final_data.to_excel(results_dir + '/' + xlsx_file_name)

for i in range(len(df['Commit_Hash'])):

	commit = df['Commit_Hash'][i]
	# os.system('rm -f !(*.csv|*.xlsx)')
	os.system("find . -type f ! -name '*.csv' -o -name '*.xlsx' -delete")
	# os.system('git checkout ' + commit)
	subprocess.check_output('git checkout ' + commit, shell = True)
	print('\n============= Covering Commit #', commit, '=============')
	all_commits_left = df.loc[df['Commit_Hash'] == commit]
	all_commits_left['index'] = (i+1)

	# Run Sub-script and generate metrics
	os.chdir(parent_directory)	
	# os.system("python3 understand_metrics_parser.py " + repo_location)
	print('Starting directory cleaning and metrics generation.....')
	subprocess.check_output("python3 understand_metrics_parser.py " + repo_location, shell=True)

	# Changing directory updates file structure, otherwise it'll give FileNotFoundError
	os.chdir(parent_directory)	
	os.chdir(repo_location)

	#Create dataframe and continue
	new_file_name_metrics = 'metrics' + commit + '.csv'
	os.rename('metrics.csv', new_file_name_metrics)
	metrics_df_right = pd.read_csv(new_file_name_metrics)
	metrics_df_right = metrics_df_right.loc[metrics_df_right['Kind'] == 'File']
	metrics_df_right = metrics_df_right[['Name', 'AvgCyclomatic', 'AvgCyclomaticModified', 'AvgCyclomaticStrict', 'AvgEssential', 'AvgLine', 'AvgLineBlank', 'AvgLineCode', 'AvgLineComment', 'CountDeclClass', 'CountDeclClassMethod', 'CountDeclClassVariable', 'CountDeclExecutableUnit', 'CountDeclFunction', 'CountDeclInstanceMethod', 'CountDeclInstanceVariable', 'CountDeclMethod', 'CountDeclMethodDefault', 'CountDeclMethodPrivate', 'CountDeclMethodProtected', 'CountDeclMethodPublic', 'CountLine', 'CountLineBlank', 'CountLineCode', 'CountLineCodeDecl', 'CountLineCodeExe', 'CountLineComment', 'CountSemicolon', 'CountStmt', 'CountStmtDecl', 'CountStmtExe', 'MaxCyclomatic', 'MaxCyclomaticModified', 'MaxCyclomaticStrict', 'MaxEssential', 'MaxNesting', 'RatioCommentToCode', 'SumCyclomatic', 'SumCyclomaticModified', 'SumCyclomaticStrict', 'SumEssential']]
	metrics_df_right.to_csv(new_file_name_metrics)

	#Part where we add per file difference column named "is_chagned"
	if i == 0:
		metrics_df_right['is_changed'] = 0
	else:
		previous_commit_filename = 'metrics' + df['Commit_Hash'][i-1] + '.csv'
		previous_commit_df = pd.read_csv(previous_commit_filename)
		req_cols_temp_df = [col for col in previous_commit_df.columns if col.lower()[:7] != 'unnamed']
		previous_commit_df = previous_commit_df[req_cols_temp_df]

		previous_commit_df.set_index('Name')
		metrics_df_right.set_index('Name')

		same_rows_idx = previous_commit_df.isin(metrics_df_right).all(1)
		# print(same_rows_idx)
		metrics_df_right['is_changed'] = (~same_rows_idx).astype(int)	
		metrics_df_right['is_changed'] =  metrics_df_right['is_changed'].fillna(1)
		time.sleep(30)


	os.chdir(parent_directory)	
	os.chdir(repo_location)
	#Add to final_data.csv
	temp_df = cartesian_product(all_commits_left, metrics_df_right)
	req_cols_temp_df = [col for col in temp_df.columns if col.lower()[:7] != 'unnamed']
	temp_df = temp_df[req_cols_temp_df]
	# temp_df.to_excel(str(i) + '.xlsx') #This is the cartesian product excel if you like to see

	final_data = pd.read_excel(results_dir + '/' + xlsx_file_name)
	req_cols_final_data = [col for col in final_data.columns if col.lower()[:7] != 'unnamed']
	final_data = final_data[req_cols_final_data]
	print('Final Data before append: ', final_data.shape)
	final_data = final_data.append(temp_df)
	print('Final Data after append: ', final_data.shape)
	print('Temp DF: ', temp_df.shape)
	# time.sleep(10)
	final_data.to_excel(results_dir + '/' + xlsx_file_name)

