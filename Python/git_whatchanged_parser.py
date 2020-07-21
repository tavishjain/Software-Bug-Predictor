import optparse, sys, os, subprocess, re, pytz
from datetime import datetime

def is_int(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

try:
    import git
    import matplotlib
    import openpyxl
    import pandas as pd
except ImportError:
    os.system("apt install python3-pip")
    os.system('apt install libncurses5')
    os.system("pip3 install gitpython")
    os.system("pip3 install pandas")
    os.system("pip3 install openpyxl==3.0.1")
    import git 
    import openpyxl
    import pandas as pd


parser  =   optparse.OptionParser()
options, args   =   parser.parse_args()

if len(args):
    path = args.pop(0)
else:
    print ("You must specify a git object as the first argument")
    sys.exit(os.EX_NOINPUT)

main_dir = os.getcwd()
repo_location = str(path)
os.chdir(repo_location)

# INPUT FEATURES
# 1. Number of File changes            - done - in files_changed
# 2. Number of LOC changes             - done - in insertions and deletions. Can calculate sum for total
# 3. Developer info                    - done - all contributions in authors 
# 4. Number of Distinct Contributors   - done - in distinct_authors
# 5. commit message                    - done - in commit_messages
# 6. Commit time difference            - done - in commit_time_diff - To calcuate the frequency of change
# 7. Size of modification              - change commit hash - in git_checkout_parser.py
# 8. Module entropy                    - change commit hash - in git_checkout_parser.py
# 9. number of defects in previous     - change commit hash - in git_checkout_parser.py
# 10. CKJM metrics                     - change commit hash - in git_checkout_parser.py

commit_hash = []
author = []
date = []
commit_message = []
files_changed = []
insertions = []
deletions = []
bug = []
commit_time_diff = []

g = git.Git(os.getcwd())
whatchanged = g.whatchanged(stat = True).split("\n")
whatchanged_iter = iter(whatchanged)

for line in whatchanged_iter:

    if line.find('commit') != -1 and len(line) == 47:
        commit_hash.append(line[7:])
        commit_message.append("")
        author.append('')
        files_changed.append(0)
        commit_time_diff.append(0)
        date.append('')
        bug.append(False)

    if line.find('Author:') != -1:
        email_id = re.findall('\S+@\S+', line) #regular expression to detect email addresses
        if len(email_id) > 0:
            email_id = email_id[0]
            email_id = email_id[1:-1]
        else:
            email_id = ""
        author.pop()
        author.append(email_id)

    if line.find('Date:') != -1:

        datetime_str = line[8:]
        datetime_object = datetime.strptime(datetime_str, '%a %b %d %H:%M:%S %Y %z')
        date.pop()
        date.append(datetime_object)

        if len(date) == 1:
            commit_time_diff.pop()
            commit_time_diff.append(0)
        else:
            seconds = date[len(date) - 2] - datetime_object
            commit_time_diff.pop()
            commit_time_diff.append(seconds.seconds)

        line = next(whatchanged_iter)
        line = next(whatchanged_iter)
        commit_message.pop()
        commit_message.append(line[4:])

    if (line.find('BUG:') != -1 or line.find('Bug:') != -1) and len(line) == 18:
        bug.pop()
        bug.append(True)

    if (line.find('file changed') != -1 or line.find('files changed') != -1) and ((line.find('insertions(+)') != -1 or line.find('insertion(+)') != -1) or (line.find('deletions(-)') != -1 or line.find('deletion(-)') != -1)):
        words = line.split(" ")
        count = 0
        for s in words:
            if is_int(s) and count == 0:
                count = count + 1
                files_changed.pop()
                files_changed.append(int(s))
                insertions.append(0)
                deletions.append(0)
            elif is_int(s) and count == 1:
                insertions.pop()
                count = count + 1
                insertions.append(int(s))
            elif is_int(s) and count == 2:
                deletions.pop()
                deletions.append(int(s))

commit_hash.reverse()
author.reverse()
date.reverse()
commit_message.reverse()
files_changed.reverse()
insertions.reverse()
deletions.reverse()
bug.reverse()
commit_time_diff.reverse()

s = set([len(commit_hash), len(commit_message), len(author), len(date), len(commit_time_diff), len(files_changed), len(insertions), len(deletions), len(bug)])
if len(s) != 1:
    sys.exit(os.EX_NOINPUT)

print("Number of commits found in the repo: ", len(commit_hash))
# print(len(commit_hash), len(commit_message), len(author), len(date), len(commit_time_diff), len(files_changed), len(insertions), len(deletions), len(bug))

df = pd.DataFrame({'Commit_Hash' : commit_hash,
                    'Author' : author,
                    'Date_Time' : date,
                    'Commit_Message' : commit_message,
                    'Files_Changed' : files_changed,
                    'Insertions' : insertions,
                    'Deletions' : deletions,
                    'Bug_present' : bug,
                    'Commit_Time_Diff' : commit_time_diff})
df['Date_Time'] = df['Date_Time'].astype(str).str[:-6]
df.to_excel('whatchanged_data.xlsx')

# for i in range(len(commit_hash))
# for i in range(3):
#     print("|||||||||||||||||||||||||||||||||| ", i, " |||||||||||||||||||||||||||||||||||||")
#     print(commit_hash[i])
#     print(commit_message[i])
#     print(author[i])
#     print(date[i])
#     print(commit_time_diff[i])
#     print(files_changed[i])
#     print(file_size_diff[i])
#     print(insertions[i])
#     print(deletions[i])
#     print(bug[i])