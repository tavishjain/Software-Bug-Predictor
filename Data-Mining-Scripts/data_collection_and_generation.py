import optparse, sys, os, subprocess, re, pytz

parser  =   optparse.OptionParser()
options, args   =   parser.parse_args()

if len(args):
    path = args.pop(0)
else:
    print ("You must specify a git repo URL as the first argument")
    sys.exit(os.EX_NOINPUT)

if os.path.isdir("logs") != True:
	os.mkdir('logs')
main_dir = os.getcwd()
curr_dir = os.getcwd() + '/logs'
os.chdir(curr_dir)
clone_command = "git clone " + path
os.system(clone_command)
os.chdir(main_dir)
if (path.split("/"))[-1] == '':
	path = (path.split("/"))[-2]
else:
	path = (path.split("/"))[-1]

path = 'logs/' + path
print('Pth: ', path)

print("\n=========== Running WHATCHANGED script ===========")
os.system("python3 git_whatchanged_parser.py " + path)

print("\n=========== Running CHECKOUT script ===========")
os.system("python3 git_checkout_parser.py " + path)

# print("\n=========== Collecting Metrics Data ===========")
# os.system("python3 understand_metrics_parser.py " + path)

# List of all collected metrics
# AvgCyclomatic, AvgCyclomaticModified, AvgCyclomaticStrict, AvgEssential, AvgLine, AvgLineBlank, AvgLineCode, AvgLineComment, CountClassBase, CountClassCoupled, CountClassCoupledModified, CountClassDerived, CountDeclClass, CountDeclClassMethod, CountDeclClassVariable, CountDeclExecutableUnit, CountDeclFile, CountDeclFunction, CountDeclInstanceMethod, CountDeclInstanceVariable, CountDeclMethod, CountDeclMethodAll, CountDeclMethodDefault, CountDeclMethodPrivate, CountDeclMethodProtected, CountDeclMethodPublic, CountInput, CountLine, CountLineBlank, CountLineCode, CountLineCodeDecl, CountLineCodeExe, CountLineComment, CountOutput, CountPath, CountPathLog, CountSemicolon, CountStmt, CountStmtDecl, CountStmtExe, Cyclomatic, CyclomaticModified, CyclomaticStrict, Essential, Knots, MaxCyclomatic, MaxCyclomaticModified, MaxCyclomaticStrict, MaxEssential, MaxEssentialKnots, MaxInheritanceTree, MaxNesting, MinEssentialKnots, PercentLackOfCohesion, PercentLackOfCohesionModified, RatioCommentToCode, SumCyclomatic, SumCyclomaticModified, SumCyclomaticStrict, SumEssential
