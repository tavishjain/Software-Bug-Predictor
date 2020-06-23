-- Do Not Edit This File.
-- [32] = default; [33] = line number; [34] = brace highlight; [35] = unmatched brace
return {
	common = {
		style = {
			caret = {
				back = "#8afff0"
			},
			comment = {
				fore = "#007f75",
				italic = true
			},
			deadcode = {
				back = "#C0C0C0"
			},
			["doc-comment"] = {
				fore = "#993300",
				italic = true
			},
			["doc-keyword"] = {
				bold = true,
				fore = "#663300",
				italic = true
			},
			["double-quoted-string"] = {
				fore = "#00ccbb"
			},
			error = {
				back = "#ff0000",
				eolfilled = true,
				fore = "#ffff00"
			},
			find = {
				back = "#ff19e3"
			},
			["fold-margin"] = {
				back = "#007f75"
			},
			identifier = {

			},
			inactive = {
				back = "#ffaa99",
				eolfilled = true
			},
			keyword = {
				bold = true,
				fore = "#267f78"
			},
			label = {
				fore = "#800000"
			},
			number = {
				fore = "#00ccbb"
			},
			operator = {
				bold = true
			},
			preprocessor = {
				bold = true,
				fore = "#00ffea"
			},
			ref = {
				back = "#cc4000"
			},
			selection = {
				back = "#00d6c1"
			},
			["single-quoted-string"] = {
				fore = "#00ccbb"
			},
			["unclosed-double-quoted-string"] = {
				back = "#ffaa99",
				eolfilled = true
			},
			["unclosed-single-quoted-string"] = {
				back = "#ffaa99",
				eolfilled = true
			},
			whitespace = {
				fore = "#808080"
			}
		}
	},
	style = {
		[32] = {
			back = "#ffffff",
			fore = "#000000"
		},
		[33] = {
			back = "#00ffea"
		},
		[34] = {
			back = "#09cc4a",
			bold = true
		},
		[35] = {
			back = "#cc1b14",
			bold = true
		}
	},
	udb = {
		style = {
			ada = {
				["global-variable"] = {
					bold = true,
					fore = "#5555ff",
					underline = true
				},
				["local-variable"] = {
					fore = "#5555ff",
					italic = true
				},
				package = {
					fore = "#005500"
				}
			},
			cs = {
				class = {
					fore = "#005500"
				},
				method = {
					fore = "#00aa00"
				}
			},
			cxx = {
				class = {
					fore = "#005500"
				},
				["function"] = {
					fore = "#00aa00"
				},
				["global-variable"] = {
					bold = true,
					fore = "#5555ff",
					underline = true
				},
				["local-variable"] = {
					fore = "#5555ff",
					italic = true
				}
			},
			fortran = {
				subprogram = {
					fore = "#00aa00"
				}
			},
			java = {
				class = {
					fore = "#005500"
				},
				method = {
					fore = "#00aa00"
				}
			},
			jovial = {
				subroutine = {
					fore = "#00aa00"
				}
			},
			pascal = {
				routine = {
					fore = "#00aa00"
				}
			},
			python = {
				class = {
					fore = "#005500"
				}
			},
			vhdl = {
				subprogram = {
					fore = "#00aa00"
				}
			}
		}
	}
}