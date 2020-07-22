#
#          Copyright (c) 2015, Scientific Toolworks, Inc.
#
# This file contains proprietary information of Scientific Toolworks, Inc.
# and is protected by federal copyright law. It may not be copied or
# distributed in any form or medium without prior written authorization
# from Scientific Toolworks, Inc.
#


package Understand::Extension;
use strict;
sub base { return "Extension"; }


# Required, language to implement or override.
sub language { return undef; }


# Required, name of extension (ie, language variant or compiler name)
sub name { return undef; }


# Implement to indicate support for parsing. Lexing must also be supported.
#
#sub parse {
#  my ($extension,$parser,$lexer) = shift;
#}
#

# Override and return true if parser is implemented and supports includes
sub parse_supports_includes { return 0; }


# Implement to indicate support for lexing.
#
#sub lex {
#  my ($extension,$lexer,$input,$line) = shift;
#}

# Override to return the list of characters allowed in editor "words".
sub editor_word_definition {
  return "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";
};

# Override to return the list of token values and the standard style names
# that they match to. Available styles: whitespace, number, identifier,
#   comment, keyword, operator, preprocessor, label, double-quoted-string,
#   single-quoted-string
sub token_styles {
#  return 0,"style0", 1,"style1", etc.;
  return undef;
};


# Callable methods on $parser:
#   entity(kind,name [,long,ext,type,link]) - returns a new entity id
#   file() - returns the entity id of the file being parsed
#   ref(kind,scope,entity,line,column) - creates a reference
#
# Callable methods on $lexer:
#   column() - return start column of current token
#   line() - return start line of current token
#   next() - advance to, and return, the next token
#   set(token,chars) - set the current token
#   text() - return text of current token
#   token() - return current token


# Called externally to create new Extension object or derivation of an Extension object.
sub new {
  my $caller = shift;
  my $class = ref($caller) || $caller;
  my $self = { @_ };
  bless($self,$class);
  return $self;
}



1;
__END__
