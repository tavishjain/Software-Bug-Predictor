import exceptions

# CLASSES

class ExpatError(builtins.Exception):
   pass

class xmlparser:
   #Methods defined here
   def ExternalEntityParserCreate(): pass
   def GetBase(): pass
   def GetInputContext(): pass
   def Parse(): pass
   def ParseFile(): pass
   def SetBase(): pass
   def SetParamEntityParsing(): pass
   def UseForeignDTD(): pass
     
XMLParserType = xmlparser
    
error = ExpatError

# FUNCTIONS
def ErrorString(): pass
def ParserCreate(): pass

# DATA
EXPAT_VERSION = 'expat_2.1.1'
XML_PARAM_ENTITY_PARSING_ALWAYS = 2
XML_PARAM_ENTITY_PARSING_NEVER = 0
XML_PARAM_ENTITY_PARSING_UNLESS_STANDALONE = 1
expat_CAPI = "pyexpat.expat_CAPI"
features = [('sizeof(XML_Char)', 1), ('sizeof(XML_LChar)', 1)]
native_encoding = 'UTF-8'
version_info = (2, 1, 1)

