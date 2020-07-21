#Print a list of the files in the project
#Todo: print the long name (ie, show directory names)
#Hint: $file is an Understand::Ent

import understand
import sys

def fileList(db):
  for file in db.ents("File"):
    #If file is from the Ada Standard library, skip to next
    if file.library() != "Standard":
      print (file.name())

if __name__ == '__main__':
  # Open Database
  args = sys.argv
  db = understand.open(args[1])
  fileList(db)    
    