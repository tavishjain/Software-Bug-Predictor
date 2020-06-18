-- TypeScript
return {
  name = "TypeScript",
  lexer = 3,
  extensions = "ts",
  keywords = {
    [0] = {
      name = "Primary Keywords",
      keywords = require "js_keywords"
    },
    [1] = {
      name = "Contextual Keywords",
      keywords =
        [[any boolean constructor declare get
        module require number set string]]
    }
  },
  style = require "cxx_styles",
  comment = {
    line = "//"
  }
}
