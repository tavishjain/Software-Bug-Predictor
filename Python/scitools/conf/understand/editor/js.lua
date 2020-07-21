-- JavaScript
return {
  name = "JavaScript",
  lexer = 3,
  extensions = "js",
  keywords = {
    [0] = {
      name = "Primary Keywords",
      keywords = require "js_keywords"
    },
    [1] = {
      name = "Secondary Keywords",
      keywords = [[]]
    }
  },
  style = require "cxx_styles",
  comment = {
    line = "//"
  }
}
