-- Extension Lexer
return {
  name = "Extension",
  lexer = 999,
  style = {
    [0] = {
      name = "Whitespace",
      style = "whitespace"
    },
    [1] = {
      name = "Number",
      style = "number"
    },
    [2] = {
      name = "Double-quoted String",
      style = "double-quoted-string"
    },
    [3] = {
      name = "Single-quoted String",
      style = "single-quoted-string"
    },
    [4] = {
      name = "Identifier",
      style = "identifier"
    },
    [5] = {
      name = "Comment",
      style = "comment"
    },
    [6] = {
      name = "Keyword",
      style = "keyword"
    },
    [7] = {
      name = "Operator",
      style = "operator"
    },
    [8] = {
      name = "Preprocessor",
      style = "preprocessor"
    },
    [9] = {
      name = "Label",
      style = "label"
    },
    [10] = {
      name = "Unclosed Double-quoted String",
      style = "unclosed-double-quoted-string"
    },
    [11] = {
      name = "Unclosed Single-quoted String",
      style = "unclosed-single-quoted-string"
    },
    [12] = {
      name = "Error",
      style = "error"
    },
    [13] = {
      name = "Doc Comment",
      style = "doc-comment"
    },
    [14] = {
      name = "Doc Keyword",
      style = "doc-keyword"
    }
  }
}
