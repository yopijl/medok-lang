import medoklang_interpreter
import medoklang_lexer
import medoklang_parser

from sys import *

#DENGAN MASUKAN BERUPA FILE DENGAN EKSTENSION .mdk
lexer = medoklang_lexer.leksikal()
parser = medoklang_parser.sintaksis()
env = {}

file = open(argv[1])
text = file.readlines()
for line in text:
    tree = parser.parse(lexer.tokenize(line))
    medoklang_interpreter.BasicExecute(tree, env)