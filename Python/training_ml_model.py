import optparse, sys, os, re, time, subprocess
from datetime import datetime
from pathlib import Path
from subprocess import *
import numpy as np
import scipy
# try:
#     import git
#     from sklearn.preprocessing import LabelEncoder
#     from sklearn.ensemble import RandomForestRegressor
#     import xlrd
#     import numpy as np
#     import pandas as pd
# except ImportError:
#     os.system("apt install python3-pip")
#     os.system("pip3 install gitpython")
#     os.system("pip3 install pandas")
#     os.system("pip3 install numpy")
#     os.system("pip3 install sklearn")
#     os.system("pip3 install xlrd")
if os.name == 'nt':
	import pygit
else:
	import git
import openpyxl
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import MinMaxScaler
import xlrd
import pandas as pd

import math
import matplotlib.pyplot as plt

parser  =   optparse.OptionParser()

options, args   =   parser.parse_args()

if len(args):
    path = args.pop(0)
else:
    print ("You must specify a git object as the first argument")
    sys.exit(os.EX_NOINPUT)
#########danger########
if os.name == 'nt':
	os.chdir(os.getcwd()+'\\Python')

parent_directory = os.getcwd()
training_dir = parent_directory + '/logs/training_data'
testing_dir = parent_directory + '/logs/testing_data'
results_dir = parent_directory + '/logs/results'

training_data_file_name = path.split('/')[-1] + '_training_data.xlsx'
testing_data_file_name = path.split('/')[-1] + '_testing_data.xlsx'
result_file_name = path.split('/')[-1] + '_result.xlsx'

summing_df = pd.read_excel(training_dir + '/' + training_data_file_name)
summing_df = summing_df[['Name', 'Bug_present']]
summing_df = summing_df.groupby(['Name'], as_index = False).sum()
# print(summing_df['Bug_present'].values)
# print(type(summing_df['Bug_present'].values))


data = pd.read_excel(training_dir + '/' + training_data_file_name) 

# Custom Class for adjusting to new and unseen labels
class LabelEncoderExt(object):
    def __init__(self):
        self.label_encoder = LabelEncoder()

    def fit(self, data_list):
        self.label_encoder = self.label_encoder.fit(list(data_list) + ['Unknown'])
        self.classes_ = self.label_encoder.classes_

        return self

    def transform(self, data_list):
        new_data_list = list(data_list)
        for unique_item in np.unique(data_list):
            if unique_item not in self.label_encoder.classes_:
                new_data_list = ['Unknown' if x==unique_item else x for x in new_data_list]

        return self.label_encoder.transform(new_data_list)
    
    def inverse_transform(self, data_list):
        return self.label_encoder.inverse_transform(data_list)

encoder = LabelEncoderExt()
encoder.fit(data['Name'].tolist())
data['Name'] = encoder.transform(data['Name'].tolist())
test_data = data.tail(len(pd.read_excel(testing_dir + '/' + path.split('/')[-1] + '_testing_data.xlsx')))
data = data.iloc[:-1*len(pd.read_excel(testing_dir + '/' + path.split('/')[-1] + '_testing_data.xlsx'))]

regressor = RandomForestRegressor(n_estimators=150, min_samples_split=2)
regressor.fit(data.drop('Bug_present', axis = 1), data['Bug_present'])

predictions = regressor.predict(test_data.drop('Bug_present', axis = 1))

colone = encoder.inverse_transform(test_data['Name']).reshape(-1, 1)
coltwo = predictions.reshape(-1, 1)

final_data = np.hstack((colone, coltwo))
final_data = pd.DataFrame(final_data, columns = ['File_Name', 'Probability'])
# print(summing_df['Bug_present'].shape)
final_data['Probability'] = pd.to_numeric(final_data['Probability'], errors='coerce')
scaler = MinMaxScaler()
final_data['Relative_Probability'] = final_data['Probability']
final_data[['Relative_Probability']] = scaler.fit_transform(final_data[['Relative_Probability']])
final_data['Probability'] = final_data['Probability'].apply(lambda x:round(x, 2))
final_data['Relative_Probability'] = final_data['Relative_Probability'].apply(lambda x:round(x, 2))
final_data['Bugs_count'] = summing_df['Bug_present']#.values.tolist()
print(final_data)
final_data.to_excel(results_dir + '/' + result_file_name)

# plt.xlabel('File_Name')
# plt.ylabel('Values')
# # plt.legend(['b', 'g', 'r'])
# plt.plot(final_data['File_Name'], final_data['Probability'], 'b', label="Probability")
# plt.plot(final_data['File_Name'], final_data['Relative_Probability'], 'g', label="Relative Probability")
# plt.plot(final_data['File_Name'], final_data['Bugs_count'], 'r', label="Bugs Count")
# plt.legend(loc="upper right")
# plt.show()

# final_data.Probability.plot(label='Probability', legend=True);
# # final_data.Relative_Probability.plot(label='Relative Probability', legend=True)
# final_data.Bugs_count.plot(secondary_y=True, label='Bugs Count', legend=True)
# # plt.show()
# plt.savefig(results_dir + '/' + path.split('/')[-1] + '_' + 'countVSprobability.png')

# final_data.Relative_Probability.plot(label='Relative Probability', legend=True)
# final_data.Bugs_count.plot(secondary_y=True, label='Bugs Count', legend=True)
# # plt.show()
# plt.savefig(results_dir + '/' + path.split('/')[-1] + '_' + 'countVSrelative_probability.png')

final_data.Probability.plot(label='Probability', legend=True);
final_data.Relative_Probability.plot(label='Relative Probability', legend=True)
final_data.Bugs_count.plot(secondary_y=True, label='Bugs Count', legend=True)
# plt.show()
plt.savefig(results_dir + '/' + path.split('/')[-1] + '_' + 'complete.png')

print(result_file_name)