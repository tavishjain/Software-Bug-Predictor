import exceptions

#Classes
class ExpatError(exceptions.Exception):
   pass
    
class xmlparser: 
   pass

XMLParserType = xmlparser
    
error = ExpatError

#Functions
def ErrorString():
   pass
    
def ParserCreate():
   pass

# DATA
EXPAT_VERSION = 'expat_2.1.0'
XML_PARAM_ENTITY_PARSING_ALWAYS = 2
XML_PARAM_ENTITY_PARSING_NEVER = 0
XML_PARAM_ENTITY_PARSING_UNLESS_STANDALONE = 1
__version__ = '2.7.11'
expat_CAPI = "pyexpat.expat_CAPI"
features = [('sizeof(XML_Char)', 1), ('sizeof(XML_LChar)', 1)]
native_encoding = 'UTF-8'
version_info = (2, 1, 0)


