import optparse, sys, os, re, time, subprocess
from datetime import datetime
from pathlib import Path
from subprocess import *

try:
    import git
    from sklearn.preprocessing import LabelEncoder
    from sklearn.ensemble import RandomForestRegressor
    import xlrd
    import numpy as np
    import pandas as pd
except ImportError:
    os.system("apt install python3-pip")
    os.system("pip3 install gitpython")
    os.system("pip3 install pandas")
    os.system("pip3 install numpy")
    os.system("pip3 install sklearn")
    os.system("pip3 install xlrd")
    import git 
    from sklearn.preprocessing import LabelEncoder
    from sklearn.ensemble import RandomForestRegressor
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
training_dir = parent_directory + "/logs/training_data"
testing_dir = parent_directory + "/logs/testing_data"
results_dir = parent_directory + "/logs/results"

training_data_file_name = path.split('/')[-1] + '_training_data.xlsx'
testing_data_file_name = path.split('/')[-1] + '_testing_data.xlsx'
result_file_name = path.split('/')[-1] + '_result.xlsx'

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
print(final_data.shape)
print(final_data)
final_data = pd.DataFrame(final_data, columns = ['File_Name', 'Probability'])
final_data.to_excel(results_dir + '/' + result_file_name)