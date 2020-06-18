#!/usr/bin/python3

import sys, os, math
import understand as und
# import cturef
import argparse
import cProfile
import json
import queue

# os.environ["UND_NAMED_ROOT_HOME_DIR"] = "/home/dmg/work"

ap = argparse.ArgumentParser()
ap.add_argument("-db", "--database", required=True,
  help="Path to .udb file of project")
ap.add_argument("-c", "--compilecommands", default=None,
  help="Path to compile_commands.json file")
ap.add_argument("-f", "--function", default=None,
  help="Function name or ID to Unify. Defaults to None which will operate on all Root Calls")
ap.add_argument("-by", "--callbys", default=False,
  help="Unification direction: False for Call references only [Default], True to Unify Calls & Callbys")
ap.add_argument("-ns", "--namespace", default=False,
  help="EXPERIMENTAL. Unravel using namespace directives.")

ap.add_argument("-d", "--debug", type=int, default=0,
  help="Debug verbosity, 0-3. 1: write debug messages to file, 2: file and console, 3: also output ents being processed")
ap.add_argument("-m", "--filemode",type=int, default=0,
  help="File mode. 1 will create a new directory structure for the Unified translation unit that mimics the original project's. 2 will write a makefile with the unified compile commands from the files concatenated for the function.")
ap.add_argument("-p", "--profile", type=bool, default=False,
  help="Profile complexity of script for debugging porpoises")
ap.add_argument("-s", "--skipC", type=bool, default=True,
  help="Skip legacy C code for compatibility porpoises")
ap.add_argument("-k", "--skipDupes", type=bool, default=False,
  help="Skip duplicate Unified code files for batch processing")
ap.add_argument("-da", "--dirAppend", default=None,
  help="Specify custom directory name suffix for duplicate unification processes")
args = vars(ap.parse_args())
dirAppend = args["dirAppend"]

# Und DB object wrapper
class UnifyDB():
  def __init__(self, db, compCmds, callbys, debug, fileMode, rootDir, skipC, unravelNamespaces):
    # Und DB object
    self.mDB = db
    # Debug verbosity
    self.mDebug = debug
    # unify by calls or add first-level callbys
    self.mUnifyCallbys = callbys
    # keep track of duplicate named functions
    self.functionNameList = []
    # compile commands dict
    self.compileCommands = compCmds
    self.fileMode = fileMode
    self.rootDir = rootDir
    self.mfTargets = []
    self.mSkipC = skipC
    self.unravelNamespaces = unravelNamespaces


  def writeMakefile(self):
    if self.fileMode > 1:
      dbName = self.mDB.name()
      dirName = dbName[:dbName.index(".")] + "_unified"
      if dirAppend:
        dirName += "_" + dirAppend
      makeFilename = dirName + "/Makefile"
      makefile = open(makeFilename, "a+", encoding="utf-8")
      makefile.write("\n\n" + "TARGETS := " + " ".join(self.mfTargets) + "\n")
      makefile.write("all: $(TARGETS)\n")
      makefile.close()


# class instance for each function being unified
class UnifyFunctionTU():
  def __init__(self, db, fxn, dupeCheck):
    # UnifyDB object
    self.mUnifyDB = db
    # Und DB object
    self.mDB = db.mDB
    # Debug verbosity
    self.mDebug = db.mDebug
    # Und function ent to unify
    self.mTarget = fxn
    self.mName = self.mTarget.name()
    # number of different same-named functions
    self.mCount = 0

    # entity lists
    self.tempCallList = []
    self.tempCallbyList = []
    # dict of all fxn longnames in project to list of IDs
    self.functionNameList = {}
    # dict of duplicate function longnames to list of IDs
    self.duplicateFunctions = {}
    # dict of file IDs to duplicate fxn IDs in file
    # self.duplicateFunctionFileLocations = {fileID:([Defines], [Calls]), fileID:(... }
    self.duplicateFunctionFileLocations = {}

    # list of all ents so can use ID as index to check if visited
    if dupeCheck:
      self.visitedEnts = []
    else:
      self.visitedEnts = list(False for _ in range(len(self.mDB.ents()) + 1))

    # keys = file ent ID. values = list of function entity IDs used in each file
    self.fileDependencyDict = {}

    # order of files visited
    self.fileOrder = []

    # self.standardTypes = ["bool", "char", "unsigned char", "signed char", "__int8", "__int16", "short", "unsigned short", "wchar_t", "__wchar_t", "float", "__int32", "int", "unsigned int", "long", "unsigned long", "double", "__int64", "long double", "long long", "uint32_t"]

    # unified include directories of all files, populated from compile commands
    if self.mUnifyDB.compileCommands:
      self.unifiedCompileCmds = ["-I" + self.mUnifyDB.rootDir]
    else:
      self.unifiedCompileCmds = []


  def dPrint(self, fxn, caller):
    if self.mDebug > 1:
      print("Adding from " + caller + ": " + str(fxn.id()) + " while processing " + fxn.name())

  def printError(self, msgList):
    print()
    for line in msgList:
      print(str(line))
    input("Press any key to continue...")


  # check params to find out if passed function is actual duplicate
  def processDupeFxn(self, targetEnt):
    targetParams = targetEnt.parameters().split(",")
    prevDupeIDs = self.functionNameList[targetEnt.longname()]
    foundDupe = [True for _ in range(len(prevDupeIDs))]
    for h in range(len(prevDupeIDs)):
      prevEnt = self.mDB.ent_from_id(prevDupeIDs[h])
      if ("Const" in targetEnt.kindname()) != ("Const" in prevEnt.kindname()):
        foundDupe[h] = False
        continue

      prevParams = prevEnt.parameters().split(",")
      foundParam = [False for _ in range(len(targetParams))]
      for i in range(len(targetParams)):
        for j in range(len(prevParams)):
          if targetParams[i] == prevParams[j]:
            del prevParams[j]
            foundParam[i] = True
            break
      for f in foundParam:
        if not f:
          foundDupe[h] = False
          continue
      if prevParams:
        foundDupe[h] = False

    for h in foundDupe:
      if h:
        return True
    return False


  # find file function was defined in and add to dependency list
  def addEnt(self, ent, caller=None):
    # check for duplicate functions
    dupe = False
    if ent.longname() not in self.functionNameList.keys():
      self.functionNameList[ent.longname()] = [ent.id()]
    else:
      dupe = self.processDupeFxn(ent)
      self.functionNameList[ent.longname()].append(ent.id())
      if dupe:
        try:
          self.duplicateFunctions[ent.longname()].append(ent.id())
        except KeyError:
          self.duplicateFunctions[ent.longname()] = [ent.id()]


    # process fxn definition location
    defin = ent.refs("Definein")
    if defin:
      # skip fxns defined in c file
      if not self.mUnifyDB.mSkipC or (self.mUnifyDB.mSkipC and not defin[0].file().name().endswith(".c")):
        definFileID = defin[0].file().id()
        if definFileID in self.fileDependencyDict.keys():
          if self.mDebug > 0:
            print("Adding " + ent.name() + " from " + defin[0].file().name())
          self.fileDependencyDict[definFileID] += [ent.id()]
        else: # first file visit
          if self.mDebug > 0:
            print("Adding", defin[0].file().name(), "while processing", self.mName)
            print("Adding " + ent.name() + " from " + defin[0].file().name())
          self.fileOrder += [definFileID]
          self.fileDependencyDict[definFileID] = [ent.id()]

        if dupe:
          if definFileID in self.duplicateFunctionFileLocations.keys():
            self.duplicateFunctionFileLocations[definFileID][0].append(ent.id())
          else:
            self.duplicateFunctionFileLocations[definFileID] = ([ent.id()],[])

          for dupeCallRef in ent.refs("Callby, Useby"):
            dCRFileID = dupeCallRef.file().id()
            if dCRFileID in self.duplicateFunctionFileLocations.keys():
              unique = True
              for prevRef in self.duplicateFunctionFileLocations[dCRFileID][1]:
                if prevRef[0] == ent.id() and prevRef[1][0] == dupeCallRef.line() - 1 and prevRef[1][1] == dupeCallRef.column():
                  unique = False
                  break
              if unique:
                self.duplicateFunctionFileLocations[dCRFileID][1].append((ent.id(), (dupeCallRef.line() - 1, dupeCallRef.column())))
            else:
              self.duplicateFunctionFileLocations[dCRFileID] = ([], [((ent.id(), (dupeCallRef.line() - 1, dupeCallRef.column())))])

      else:
        if self.mDebug > 0:
          print("C file skipped: ", defin[0].file().name())
    elif self.mUnifyDB.mDebug > 1:
      print("No defin for:", ent.name())


  def exploreCalls(self, startEnt, callRefType, callEntType):
    Q = queue.Queue(maxsize=len(self.visitedEnts))
    self.visitedEnts[startEnt.id()] = True
    Q.put(startEnt, False)

    while not Q.empty():
      currentEnt = Q.get(False)
      for callee in currentEnt.refs(callRefType, callEntType, True):
        if not self.visitedEnts[callee.ent().id()]:
          self.visitedEnts[callee.ent().id()] = True
          self.tempCallList.append(callee.ent())
          Q.put(callee.ent(), False)


  def exploreCallbys(self, startEnt, callbyRefType, callbyEntType):
    Q = queue.Queue(maxsize=len(self.visitedEnts))
    self.visitedEnts[startEnt.id()] = True
    Q.put(startEnt, False)

    while not Q.empty():
      currentEnt = Q.get(False)
      for callby in currentEnt.refs(callbyRefType, callbyEntType):
        if not self.visitedEnts[callby.ent().id()]:
          self.visitedEnts[callby.ent().id()] = True
          self.tempCallbyList.append(callby.ent())
          Q.put(callby.ent(), False)


  def unifyFunction(self, fxnEnt, fromCall, isRootFxn=False):
    if not self.visitedEnts[fxnEnt.id()] or fromCall:
      self.tempCallList = []
      self.exploreCalls(fxnEnt, "Call, Use", "~Unresolved Function")
      if self.tempCallList:
        # reverse call order
        self.tempCallList = self.tempCallList[::-1]
        for call in self.tempCallList:
          self.addEnt(call, "uF Calls")

      # only unify callbys of root fxn
      if self.mUnifyDB.mUnifyCallbys and isRootFxn:
        self.tempCallbyList = []
        self.exploreCallbys(fxnEnt, "Callby", "Function")
        if self.tempCallbyList:
          for callby in self.tempCallbyList:
            self.unifyFunction(callby, True)

      self.dPrint(fxnEnt, "unifyFunction")
      self.addEnt(fxnEnt, "uF End")


  # handle include paths in compile cmds
  def translateIncludePath(self, inclPath):
    if inclPath.startswith("-I") or inclPath.startswith("-isystem"):
      rootPath = self.mUnifyDB.rootDir
      isystem = False
      strippedPath = inclPath

      if strippedPath.startswith("-isystem"):
        strippedPath = inclPath.split()[1]
        isystem = True
      else:
        strippedPath = strippedPath.replace("-I", "")

      if not strippedPath.startswith("/"):
        depth = strippedPath.count("../")
        newRoot = "/".join(rootPath.split("/")[::-1][depth:][::-1])
        strippedPath = strippedPath.replace("../", "")
        if isystem:
          return "-isystem " + newRoot + "/" + strippedPath
        else:
          return "-I" + newRoot + "/" + strippedPath
    return inclPath


  # unify dependencies of inline defined member fxns
  def unifyClass(self, classEnt):
    if not self.visitedEnts[classEnt.id()]:
      fxnDefs = classEnt.refs("Define", "Function")
      for fD in fxnDefs:
        if fD.ent().freetext("Inline"):
          if self.mDebug > 0:
            print("unifying from class: ", fD.ent().name())
          self.unifyFunction(fD.ent(), False)
      self.visitedEnts[classEnt.id()] = True


  # cull unvisited functions from file and write to new unified object
  def unifyFile(self, targetFile):
    if self.mUnifyDB.compileCommands:
      # creates short filename with first five dir levels eg dep/libssh2/libssh2/src/openssl.c
      mediumName = '/'.join(targetFile.longname().split("/")[::-1][:5][::-1])
      if mediumName in self.mUnifyDB.compileCommands.keys():
        fileCmdList = self.mUnifyDB.compileCommands[mediumName].split()
        for i in range(len(fileCmdList)):
          if fileCmdList[i] == "-isystem":
            inclCmd = self.translateIncludePath(" ".join(fileCmdList[i:i+2]))
            self.unifiedCompileCmds.append(inclCmd)
          elif fileCmdList[i].startswith("-I") or fileCmdList[i].startswith("-D"):
            if ":" not in fileCmdList[i]: # : not compatible with make
              inclCmd = self.translateIncludePath(fileCmdList[i])
              self.unifiedCompileCmds.append(inclCmd)

    splitFile = targetFile.contents().splitlines()

    # replace includes with full include path name
    fileIncludes = targetFile.refs("Include", "~Unresolved")
    for incl in fileIncludes:
      splitFile[incl.line() - 1] = "#include <" + incl.ent().longname() + ">"

    # keep track of file-wide line modifications and offset required
    lineMods = {}

    # create custom namespace for previously file-scope global objects and update references
    for gODefineRef in targetFile.filerefs("Define", "Static Global Object"):
      comment = ""
      try:
        ind = splitFile[gODefineRef.line() - 1].index("//")
        comment = splitFile[gODefineRef.line() - 1][ind:]
        splitFile[gODefineRef.line() - 1] = splitFile[gODefineRef.line() - 1][:ind].strip()
      except ValueError:
        pass

      gOName = gODefineRef.ent().name()
      defLine = gODefineRef.line() - 1
      gONamespaceName = targetFile.name().replace(".","_") + "__" + gOName

      defInMacro = False
      if gODefineRef.ent().freetext("DefinedInMacro"):
        defInMacro = True`

      oldLine = splitFile[defLine]

      if splitFile[defLine].endswith(";"):
        splitFile[defLine] = "namespace " + gONamespaceName + " { " + splitFile[defLine] + " }; " + comment
      else:
        # define ref at end of struct typedef
        if splitFile[defLine].startswith("}"):
          # TODO: and type is struct?
          while "{" not in splitFile[defLine]:
            defLine -= 1

        splitFile[defLine] = "namespace " + gONamespaceName + " { " + splitFile[defLine]

        startOfOrigDef = len(splitFile[defLine]) - len(oldLine)
        endLine = defLine
        block = False
        # TODO: split out comments
        while not (splitFile[endLine].endswith(");") or splitFile[endLine].endswith("};") or (defInMacro and splitFile[endLine].endswith(")"))):
          # handle multi-line inline declarations
          if "{" in splitFile[endLine][startOfOrigDef:]:
            block = True
          if splitFile[endLine].endswith(";") and not block:
            break
          endLine += 1

          if endLine == len(splitFile):
            self.printError(["Could not find end to:", splitFile[defLine], targetFile.name(), defLine, gODefineRef.ent(), gODefineRef.ent().id()])

        splitFile[endLine] += " }; " + comment

      for gOUseRef in gODefineRef.ent().refs("Setby, Useby, Modifyby, Callby"):
        refLine, refCol = gOUseRef.line() - 1, gOUseRef.column()
        if refLine == defLine:
          continue

        # add entry for line modification
        if refLine in lineMods.keys():
          for lm in lineMods[refLine]:
            if lm[0] < refCol:
              refCol += lm[1]
          lineMods[refLine].append((refCol, len(gONamespaceName) + 2))
        else:
          lineMods[refLine] = [(refCol, len(gONamespaceName) + 2)]

        # insert custom scoped namespace
        try:
          splitFile[refLine] = splitFile[refLine][:refCol] + gONamespaceName + "::" + splitFile[refLine][refCol:]
        except IndexError:
          self.printError(["GOUse IndexError", gOUseRef.ent(), targetFile.name(), refLine, len(splitFile), splitFile[len(splitFile)-5:]])

    # unify inline called functions in file
    for cFR in targetFile.filerefs("Call"):
      if not self.visitedEnts[cFR.ent().id()]:
        if cFR.scope().kindname() == "Namespace" or cFR.scope().kindname() == "File":
          self.unifyFunction(cFR.ent(), False)

    # process duplicate functions
    if targetFile.id() in self.duplicateFunctionFileLocations.keys():
      defineIDs = self.duplicateFunctionFileLocations[targetFile.id()][0]
      for dID in defineIDs:
        dupeFxn = self.mDB.ent_from_id(dID)
        defLine, startOfName = dupeFxn.refs("Definein")[0].line() - 1, dupeFxn.refs("Definein")[0].column()
        dupeFxnNum = str(self.duplicateFunctions[dupeFxn.longname()].index(dID))

        splitFile[defLine] = splitFile[defLine][:startOfName] + splitFile[defLine][startOfName:].replace(dupeFxn.name(), dupeFxn.name() + dupeFxnNum, 1)

        if self.mDebug > 0 and splitFile[defLine][startOfName + len(dupeFxn.name())] != dupeFxnNum[0]:
          print("Check altered line for correctness: " + targetFile.name() + " line " + refLine + ":")
          print(splitFile[refLine])

      callbyLocationTuples = self.duplicateFunctionFileLocations[targetFile.id()][1]
      for locTuple in callbyLocationTuples:
        dID = locTuple[0]
        dupeFxn = self.mDB.ent_from_id(dID)
        dupeFxnNum = str(self.duplicateFunctions[dupeFxn.longname()].index(dID))
        refLine, startOfName = locTuple[1][0], locTuple[1][1]

        if refLine in lineMods.keys():
          for lm in lineMods[refLine]:
            if lm[0] < startOfName:
              startOfName += lm[1]
          lineMods[refLine].append((startOfName, len(dupeFxnNum)))
        else:
          lineMods[refLine] = [(startOfName, len(dupeFxnNum))]

        splitFile[refLine] = splitFile[refLine][:startOfName] + splitFile[refLine][startOfName:].replace(dupeFxn.name(), dupeFxn.name() + dupeFxnNum, 1)

        if self.mDebug > 0 and (splitFile[refLine][startOfName + len(dupeFxn.name())] != dupeFxnNum[0] or splitFile[refLine][splitFile[refLine].index(dupeFxn.name()) + len(dupeFxn.name())] != dupeFxnNum[0]):
          print("Check altered line for correctness: " + targetFile.name() + " line " + refLine + ":")
          print(splitFile[refLine])

    # list of fxns in file found by unification
    fxnsUsed = self.fileDependencyDict[targetFile.id()]

    # function preprocessing to add various functions required for compilation to call tree
    for bRef in targetFile.filerefs("Begin", "Virtual Function", True):
      if not self.visitedEnts[bRef.ent().id()]:
        if bRef.ent().refs("Overrides"):
          self.unifyFunction(bRef.ent(), False)

    beginRefs = targetFile.filerefs("Begin", "~Lambda Function", True)
    endRefs = targetFile.filerefs("End", "~Lambda Function", True)

    beginClassRefs = targetFile.filerefs("Begin", "Class, Struct", True)
    for bR in beginClassRefs:
      self.unifyClass(bR.ent())


########################################
# WIP CODE
########################################


    # undo namespace using-directives and scope references accordingly
    if self.mUnifyDB.unravelNamespaces:
      declaredNS = list(ref.ent().name() for ref in targetFile.filerefs("Declare", "Namespace"))
      usingRefs, usingEnts, usingNames = targetFile.filerefs("Using", "Namespace"), [], []
      usingNSstd = False

      for nsRef in usingRefs:
        splitFile[nsRef.line() - 1] = "CULL"
        if nsRef.ent().name() == "std":
          usingNSstd = True
        else:
          usingEnts.append(nsRef.ent())
          usingNames.append(nsRef.ent().name())

      matchingRefs = []

      # handle separately
      if usingNSstd:
        matchingRefs += list(ref for ref in targetFile.filerefs("Typed, Type", "~Function") if ref.ent().parent().longname().startswith("std"))
        matchingRefs += list(ref for ref in targetFile.filerefs("Call", "~Const Function") if ref.ent().parent().longname().startswith("std"))
        matchingRefs.append("ENDSTDREFS")

      if usingEnts or matchingRefs:
        enumRefs = targetFile.filerefs("Use", "Enumerator")
        allRefs = targetFile.filerefs("Name, Typed, Type, Call ~Implicit")
        matchingRefs += list(ref for ref in enumRefs if ref.ent().parent().parent() in usingEnts)
        matchingRefs += list(ref for ref in allRefs if ref.ent().parent() in usingEnts)

        handlingStdRefs = usingNSstd
        for mR in matchingRefs:
          if handlingStdRefs and mR == "ENDSTDREFS":
            handlingStdRefs = False
            continue

          name = mR.ent().name()
          if not name.startswith("operator") and not name.startswith("~"):
            refLine, refCol = mR.line() - 1, mR.column()

            if handlingStdRefs:
              parentName = "std"
              if mR.ent().parent().name() == "basic_string":
                name = "string"
            elif mR.ent().parent() not in usingEnts and "Enum" in mR.ent().kind().longname():
              parentName = mR.ent().parent().parent().name()
            else:
              parentName = mR.ent().parent().name()

            if refLine in lineMods.keys():
              for lm in lineMods[refLine]:
                if lm[0] < refCol:
                  refCol += lm[1]
            else:
              lineMods[refLine] = []

            # ref column in middle of "::"
            if splitFile[refLine][refCol] == ":":
              refCol += 1

            replacementString = parentName + "::" + name
            oldLine = splitFile[refLine]

            # look for namespace already scoped with all possible parent combinations
            if handlingStdRefs:
              possibleStrings = [replacementString, name]
              shortnameIdx = 1
            else:
              longname = mR.ent().longname()
              possibleStrings = []
              splitName = longname.split("::")
              for i in range(1, len(splitName) + 1):
                possibleStrings.append("::".join(splitName[len(splitName) - i:]))
              try:
                shortnameIdx = possibleStrings.index(name)
              except ValueError:
                shortnameIdx = -1

            found = -1 #idx in possStr
            for i in range(len(possibleStrings)):
              offsetCol = refCol - (len(possibleStrings[i]) - len(name)) - 1
              idx = splitFile[refLine].find(possibleStrings[i])
              if idx >= 0 and idx != shortnameIdx:
                found = i
                break

            if replacementString == possibleStrings[found]:
              continue

            # found w/ some scoped version of longname other than bare
            if found >= 0:
              name = possibleStrings[found]
              replacementString = parentName + "::" + name

            splitFile[refLine] = splitFile[refLine][:refCol] + splitFile[refLine][refCol:].replace(name, replacementString, 1)

            dist = len(splitFile[refLine]) - len(oldLine)
            lineMods[refLine].append((refCol, dist))

            if dist == 0:
              if self.mDebug > 0:
                self.printError([
                  "std::std::",
                  name,
                  found,
                  replacementString,
                  shortnameIdx,
                  possibleStrings[found],
                  possibleStrings,
                  targetFile.name(),
                  mR.ent(),
                  mR.ent().kind().longname(),
                  mR.ent().parent(),
                  mR.ent().parent().kind().longname(),
                  mR.kind().longname(),
                  mR.scope(),
                  str(refLine + 1) + ", " + str(refCol),
                  oldLine,
                  splitFile[refLine]
                  ])


########################################
# END WIP CODE
########################################


    # get list of all functions in a file, cull those not used
    for bRef in beginRefs:
      fxnID = bRef.ent().id()
      if fxnID not in fxnsUsed:
        definStart = bRef.line() - 1
        definEnd = [ref.line() for ref in endRefs if ref.ent().id() == fxnID][0]
        for i in range(definStart, definEnd):
          splitFile[i] = "CULL"

    # ! LINES IN FILE REMOVED HERE !
    splitFile[:] = [line for line in splitFile if line != "CULL"]

    # trim excess whitespace
    for i in range(len(splitFile) - 1, -1, -1):
      if splitFile[i] == "" and splitFile[i-1] == "":
        del splitFile[i]

    # undefine single-file-defined macros
    macroRefs = targetFile.refs("Define", "Macro")
    if macroRefs:
      for mR in macroRefs:
        splitFile.append("#undef " + mR.ent().name() + "\n")

    # macros to manually undefine case-by-case
    # manualUndefs = ["max", "min"]
    # for mU in manualUndefs:
    #   splitFile.append("#undef " + mU + "\n")

    return splitFile


  def getUnifiedFilename(self, skipMode):
    # checks for multiple same-named functions, renames if so
    for name in self.mUnifyDB.functionNameList:
      if name.startswith(self.mName):
        self.mCount += 1
    if self.mCount > 0:
      self.mName += str(self.mCount)
    self.mUnifyDB.functionNameList.append(self.mName)

    dbName = self.mDB.name()
    fxnName = self.mTarget.longname().replace("::", "_")

    # keep special characters out of filenames and Makefile entries
    fxnName = fxnName.replace("=", "_EQ_")
    fxnName = fxnName.replace(" ", "_")
    fxnName = fxnName.replace("!", "_NOT_")
    fxnName = fxnName.replace("*", "_STAR_")
    fxnName = fxnName.replace(">", "_GRTR_")
    fxnName = fxnName.replace("<", "_LESS_")
    fxnName = fxnName.replace("|", "_OR_")
    fxnName = fxnName.replace("&", "_AND_")
    fxnName = fxnName.replace("(", "_LPAREN_")
    fxnName = fxnName.replace(")", "_RPAREN_")
    fxnName = fxnName.replace("/", "_BKSLSH_")
    fxnName = fxnName.replace("\\", "_FWSLSH_")

    if self.mCount > 0:
      fxnName += str(self.mCount)

    # filename = projectname/functionname_unified.cpp
    fileExt = ".cpp"
    dirName = dbName[:dbName.index(".")] + "_unified"
    if dirAppend:
      dirName += "_" + dirAppend

    if not os.path.exists(dirName):
      os.mkdir(dirName)

    unifiedFilename = dirName + "/" + fxnName + fileExt

    if skipMode:
      return os.path.exists(unifiedFilename)
    return fxnName, dirName


  def unifyFiles(self):
    #output list of source files unified in project
    if self.mDebug > 0:
      fout = open("filesoutput.txt", "w+")
      for fID in self.fileOrder:
        fEnt = self.mDB.ent_from_id(fID)
        if fEnt.name().endswith(".cpp"):
          fout.write(fEnt.longname() + "\n")
      fout.close()

    fileExt = ".cpp"
    fxnName, dirName = self.getUnifiedFilename(False)
    unifiedFilename = dirName + "/" + fxnName + fileExt

    codeFile = open(unifiedFilename, "w+", encoding="utf-8")
    for fID in self.fileOrder:
      fEnt = self.mDB.ent_from_id(fID)
      if "Header" not in fEnt.kind().longname():
        codeFile.write("\n\n// Added from: " + fEnt.relname() + '\n\n')
        # codeFile.write("\n\nnamespace {\n\n)
        for line in self.unifyFile(fEnt):
          codeFile.write(line + '\n')
        # codeFile.write("\n\n}\n\n")
    codeFile.close()

    # add makefile entry for unified compile commands
    if self.unifiedCompileCmds and self.mUnifyDB.fileMode > 1:
      self.unifiedCompileCmds = list(dict.fromkeys(self.unifiedCompileCmds))
      compileCmdStr = ""
      for item in self.unifiedCompileCmds:
        compileCmdStr += item + " "
      makeFilename = dirName + "/Makefile"
      makefile = open(makeFilename, "a+", encoding="utf-8")
      makefile.write("\n" + fxnName + ": " + fxnName + fileExt + "\n")
      makefile.write("	$(CXX) $(CXXFLAGS) " + compileCmdStr + " -c $^\n")
      makefile.close()
      self.mUnifyDB.mfTargets.append(fxnName)

    print("Done writing " + unifiedFilename)


##################################


# get all functions without callbys or lambda (fxn inside a fxn)
def getRootCalls(db):
  rootCalls = []
  allFxns = db.ents("Function ~Unresolved ~Lambda")
  for f in allFxns:
    callbys = f.refs("Callby", "~Unresolved")
    if not callbys:
      rootCalls.append(f)
  return rootCalls


def main():
  debug = args["debug"]
  db = und.open(args["database"])
  fxnToUnify = args["function"]
  callbys = args["callbys"]
  fileMode = args["filemode"]
  skipC = args["skipC"]
  unravelNamespaces = args["namespace"]
  skipDupes = args["skipDupes"]
  compCmdsFile = args["compilecommands"]
  compCmdDict = {}
  rootDir = []
  if compCmdsFile:
    compCmdList = json.load(open(compCmdsFile))
    for item in compCmdList:
      if item["directory"] not in rootDir:
        rootDir.append(item["directory"])
      compCmdDict['/'.join(item["file"].split("/")[::-1][:5][::-1])] = item["command"]

    assert len(rootDir) == 1, "Multiple root directories found: " + ", ".join(rootDir)
    rootDir = rootDir[0]

  assert "C++" in db.language(), "Project does not use C/C++"

  if debug:
    print("Debug Enabled")
    # cturef.writeAllEnts(db)

  uDB = UnifyDB(db, compCmdDict, callbys, debug, fileMode, rootDir, skipC, unravelNamespaces)

  # look up specific fxn(s) by name
  if fxnToUnify:
    fxnList = db.lookup("^" + fxnToUnify + "$", "Function")
  # operate on root calls of fxn
  else:
    fxnList = getRootCalls(db)

  numRC = 0
  totalRC = len(fxnList)
  for fxn in fxnList:
    uFxn = UnifyFunctionTU(uDB, fxn, skipDupes)

    if skipDupes:
      # piggybacks on file that handles fxn filename formatting to check if file exists, skips if so
      if uFxn.getUnifiedFilename(True):
        continue

    uFxn.unifyFunction(fxn, True, True)
    uFxn.unifyFiles()

    numRC += 1
    if totalRC > 10 and numRC % (totalRC // 10) == 0:
      print(str(math.ceil((numRC / totalRC) * 100)) + "%")

  if fileMode > 1:
    uDB.writeMakefile()

  db.close()

if __name__ == "__main__":
  if args["profile"]:
    cProfile.run('main()')
  else:
    main()
