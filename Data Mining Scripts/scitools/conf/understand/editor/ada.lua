-- Ada
return {
  name = "Ada",
  lexer = 20,
  extensions = "ads,adb",
  keywords = {
    [0] = {
      name = "Keywords",
      keywords =
        [[abort abs abstract accept access aliased all and array
        at begin body case constant declare delay delta digits
        do else elsif end entry exception exit for function generic
        goto if in is limited loop mod new not null of or others
        out package pragma private procedure protected raise range
        record rem renames requeue return reverse select separate
        subtype tagged task terminate then type until use when
        while with xor]]
    },
    [1] = {
      name = "Doc Keywords",
      keyword =
        [[abstract accept and assert check derives end from global
        hide hold in inherit initializes invariant is main_program
        out own post pre protected return some task type null]]
    }
  },
  style = {
    [1] = {
      name = "Keyword",
      style = "keyword"
    },
    [2] = {
      name = "Identifier",
      style = "identifier"
    },
    [3] = {
      name = "Number",
      style = "number"
    },
    [4] = {
      name = "Operator",
      style = "operator"
    },
    [5] = {
      name = "Character",
      style = "single-quoted-string"
    },
    [6] = {
      name = "Unclosed Character",
      style = "unclosed-single-quoted-string"
    },
    [7] = {
      name = "String",
      style = "double-quoted-string"
    },
    [8] = {
      name = "Unclosed String",
      style = "unclosed-double-quoted-string"
    },
    [9] = {
      name = "Label",
      style = "label"
    },
    [10] = {
      name = "Comment",
      style = "comment"
    },
    [11] = {
      name = "Illegal Token",
      style = "error"
    },
    [12] = {
      name = "Doc Comment",
      style = "doc-comment"
    },
    [13] = {
      name = "Doc Keyword",
      style = "doc-keyword"
    }
  },
  match = {
    keyword = {
      start = "begin if elsif else loop while for case",
      ["end"] = "end elsif else"
    }
  },
  comment = {
    line = "--"
  }
}
