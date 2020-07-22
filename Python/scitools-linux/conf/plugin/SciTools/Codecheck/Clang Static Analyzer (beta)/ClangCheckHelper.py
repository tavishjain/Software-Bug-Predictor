#!/usr/bin/env python3

# Helper function to grab Clang Check information from web in the following format:
# Name: <span class="name">core.StackAddressEscape</span>
# Lang: <span class="lang">(C)</span>
# Desc: <div class="descr">Check that addresses of stack memory do not escape the function.</div>
#
# Example: <div class="example"><pre>
#char const *p;
#
#void test() {
#  char const str[] = "string";
#  p = str; // warn
#}
#</pre></div>

import requests
from bs4 import BeautifulSoup
import os
import sys
import pickle

def chomp(x): # strip newlines
  x = str(x)
  if x.endswith("\r\n"):
    return x[:-2]
  if x.endswith("\n") or x.endswith("\r"):
    return x[:-1]
  return x


def processLang(name, lang):
  if name == "cplusplus.InnerPointer":
    lang = "(C++)"
  elif name == "optin.performance.GCDAntipattern":
    lang = "(ObjC)"
  elif name == "optin.portability.UnixAPI":
    lang = "(C)"
  elif name.startswith("osx.cocoa"):
    lang = "(ObjC)"

  lang = lang.replace(",C", ", C")
  return lang


def processDescription(name, desc):
  desc = desc.replace("MPI", "Message Passing Interface")
  desc = desc.replace("Grand Central Dispatch", "Grand Central Dispatch in OSX or iOS")
  desc = desc.replace("drand48", " drand48")
  if name == "core.VLASize":
    desc = "Check for declarations of Variable Length Arrays of undefined or zero size."

  desc = desc.replace('\n', ' ')
  desc = desc.strip()
  return desc


def getChecks():
  if os.path.exists("checks.htm"):
    print("Checks file found.")
    try:
      fin = open("checks.htm", "r")
    except IOError:
      print("Could not open checks.htm file to read. Exiting.")
      sys.exit(1)
    checkData = fin.read()
  else:
    print("Checks file not found, getting from web...")
    r = requests.get('https://clang.llvm.org/docs/analyzer/checkers.html')
    try:
      fout = open("checks.htm", "w+")
    except IOError:
      print("Could not open checks.htm file to write. Exiting.")
      sys.exit(1)
    r.encoding = 'utf-8'
    checkData = r.text
    fout.write(checkData)

  soup = BeautifulSoup(checkData, features="html.parser")

  nameList = []
  checkList = []
  # check = [id, name, lang, basicdesc, detaileddesc, example]

  secList = soup.find_all(class_="section")

  for section in secList: # div class="section" for each check
    header = section.find('a').string

    check = []
    check = header.split(" ", 2)
    if len(check[0]) < 7:
      continue
    if len(check) < 3:
      check.append("")

    #Descriptions
    basicdesc = ""
    detaildesc = ""
    descBQ = section.find("blockquote")
    descP = section.find("p")

    if descBQ is None and descP is None:
      continue

    if descBQ is not None and descP is not None:
      basicdesc = chomp(descP.string)
      detaildesc = basicdesc[:] + " "
      for item in descBQ.contents:
        detaildesc += chomp(item)

    if descBQ is None and descP is not None:
      if descP.string is None:
        if ':' in descP.contents[0]:
          basicdesc = chomp(descP.contents[0])
          basicdesc = basicdesc.replace(":", ".")
        else:
          for item in descP.strings:
            basicdesc += chomp(item)
        for item in descP.contents:
          detaildesc += chomp(item)
      else:
        basicdesc = chomp(descP.string)
        detaildesc = basicdesc

    if descBQ is not None and descP is None:
      basicdesc = descBQ.find("div")
      if basicdesc.string is None:
        for item in basicdesc.contents:
          detaildesc += chomp(item)
        basicdesc = chomp(basicdesc.contents[0])
        basicdesc = basicdesc.replace(":", ".")
      else:
        basicdesc = chomp(basicdesc.string)
        detaildesc = basicdesc

    check[2] = processLang(check[1], check[2])
    basicdesc = processDescription(check[1], basicdesc)
    detaildesc = processDescription(check[1], detaildesc)
    check.append(basicdesc)
    check.append(detaildesc)

    #Examples
    ex = ""
    examples = section.find(class_="highlight")
    ex = str(examples)
    check.append(ex)

    nameList.append(check[1])
    checkList.append(check)

  try:
    fout = open("checks.txt", "wb")
    nout = open("checknames.txt", "w+")
  except IOError:
    print("Error, could not open checks.txt file to write")
    sys.exit(1)

  pickle.dump(checkList, fout)
  for name in nameList:
    nout.write(name + "\n")
  fout.close()
  nout.close()
  print("Checks written to checks.txt, names written to checknames.txt")
  return


def putChecks():
  if os.path.exists("checks.txt"):
    print("Checks file found.")
    try:
      fin = open("checks.txt", "rb")
    except IOError:
      print("Could not open checks.txt file to read. Exiting.")
      sys.exit(1)
  else:
    print("Checks.txt file not found. Run with option 'g' first.")
    return

  checkData = pickle.load(fin)
  fin.close()

  for check in checkData:
    path = ""
    cID = ""
    name = ""
    lang = ""
    bdesc = ""
    ddesc = ""
    examples = ""

    cID = check[0]
    name = check[1]
    lang = check[2]
    bdesc = check[3]
    ddesc = check[4]
    examples = check[5]

    # path = name[:]
    path = name.replace('.', '/')

    try:
      txtout = open(path + ".txt", "w+")
    except IOError:
      print(path + "Could not open description txt file to write. Exiting.")
      sys.exit(1)

    txtout.write(lang + " " + bdesc)

    try:
      htmout = open(path + ".htm", "w+")
    except IOError:
      print("Could not open description htm file to write. Exiting.")
      sys.exit(1)
    
    htmout.write("<p><b>" + cID + " " + name + " " + lang + "</b><br>\n")
    htmout.write(ddesc + "</p>\n")
    if examples != "None":
      htmout.write("<p>Examples:\n")
      htmout.write('<pre>' + examples + "</pre></p>")

    txtout.close()
    htmout.close()
  
  print("All check txt and htm files written.")
  return


def matchMISRAandClang():
  matches = [
    ("1.1.3.1.", "CPP08 Rule 0-1-3"),
    ("1.1.3.1.", "CPP08 Rule 0-1-9"),
    ("1.1.6.1.", "CPP08 Rule 6-5-1"),
    ("1.2.2.8.", "CPP08 Rule 5-0-15"), # Alpha
    ("1.2.2.9.", "CPP08 Rule 5-0-17"), # Alpha
    ("1.2.4.1.", "CPP08 Rule 0-1-1"), # Alpha
    ("1.2.4.1.", "CPP08 Rule 0-1-9"), # Alpha
    ("1.1.1.6.", "C04 1.2"),
    ("1.1.1.12.", "C04 1.2"),
    ("1.1.6.1.", "C04 13.4"),
    ("1.2.4.1.", "C04 14.1"), # Alpha
    ("1.2.2.8.", "C04 17.1"), # Alpha
    ("1.2.2.9.", "C04 17.2"), # Alpha
    ("1.2.2.8.", "C04 17.4"), # Alpha
    ("1.1.1.6.", "C12 Rule 1.3"),
    ("1.1.1.12.", "C12 Rule 1.3"),
    ("1.1.3.1.", "C12 Rule 2.2"),
    ("1.1.6.1.", "C12 Rule 14.1"),
    ("1.2.2.8.", "C12 Rule 18.1"), # Alpha
    ("1.2.2.9.", "C12 Rule 18.2"), # Alpha
    ("1.1.1.7.", "C12 Rule 18.8"),
    ]

  # TODO - write matches to CSV file

  return


def main():
  # Can use with ./DescriptionHelper.py g
  if len(sys.argv) > 1:
    if sys.argv[1] == "g":
      getChecks()
      exit(0)
    elif sys.argv[1] == "p":
      putChecks()
      exit(0)
    elif sys.argv[1] == "a":
      getChecks()
      putChecks()
      exit(0)

  print("Welcome to the Clang Check Description Helper.")
  print("Enter g to get Check info from file or web.")
  print("Enter p to populate local directory tree from file processed with 'g'.")
  print("Enter x to exit.")
  choice = ""
  while choice == "":
    choice = input("Enter choice: ")
    if choice == "g":
      getChecks()
      choice = ""
    if choice == "p":
      putChecks()
      choice = ""
    if choice == "x":
      sys.exit(0)
    else:
      choice = ""

if __name__ == "__main__":
  main()
