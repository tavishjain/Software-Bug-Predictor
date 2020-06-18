-- Visual Basic
return {
  name = "Visual Basic",
  lexer = 8,
  extensions = "vb",
  keywords = {
    [0] = {
      name = "Keywords",
      keywords =
        [[addhandler addressof alias and andalso as boolean byref byte byval
        call case catch cbool cbyte cchar cdate cdec cdbl char cint class
        clng cobj const continue csbyte cshort csng cstr ctype cuint culng
        cushort date decimal declare default delegate dim directcast do
        double each else elseif end endif enum erase error event exit false
        finally for friend function get gettype getxmlnamespace global gosub
        goto handles if implements imports in inherits integer interface is
        isnot let lib like long loop me mod module mustinherit mustoverride
        mybase myclass namespace narrowing new next not nothing notinheritable
        notoverridable object of on operator option optional or orelse
        overloads overridable overrides paramarray partial private property
        protected public raiseevent readonly redim rem removehandler resume
        return sbyte select set shadows shared short single static step stop
        string structure sub synclock then throw to true try trycast typeof
        variant wend uinteger ulong ushort using when while widening with
        withevents writeonly xor]]
    }
  },
  style = {
    [1] = {
      name = "Comment",
      style = "comment"
    },
    [2] = {
      name = "Number",
      style = "number"
    },
    [3] = {
      name = "Keyword",
      style = "keyword"
    },
    [4] = {
      name = "String",
      style = "double-quoted-string"
    },
    [5] = {
      name = "Preprocessor",
      style = "preprocessor"
    },
    [6] = {
      name = "Operator",
      style = "operator"
    },
    [7] = {
      name = "Identifier",
      style = "identifier"
    },
    [8] = {
      name = "Date",
      style = "double-quoted-string"
    },
    [9] = {
      name = "Unclosed String",
      style = "unclosedDoubledQuotedString"
    },
    [10] = {
      name = "Keyword 2",
      style = "keyword"
    },
    [11] = {
      name = "Keyword 3",
      style = "keyword"
    },
    [12] = {
      name = "Keyword 4",
      style = "keyword"
    },
    [13] = {
      name = "Constant",
      style = "keyword"
    },
    [14] = {
      name = "Inline Asm",
      style = "single-quoted-string"
    },
    [15] = {
      name = "Label",
      style = "label"
    },
    [16] = {
      name = "Error",
      style = "error"
    },
    [17] = {
      name = "Hexadecimal Number",
      style = "number"
    },
    [18] = {
      name = "Binary Number",
      style = "number"
    }
  },
  comment = {
    line = "'"
  }
}
