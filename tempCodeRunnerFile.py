import medoklang_interpreter
import medoklang_lexer
import medoklang_parser

from sys import *

#MASUKAN LANGSUNG DENGAN TERMINAL PADA PROGRAM
if __name__ == '__main__':
    lexer = medoklang_lexer.leksikal()
    parser = medoklang_parser.sintaksis()
    env = {}
    while True:
        try:
            text = input('medok > ')
        except EOFError:
            break
        if text:
            tree = parser.parse(lexer.tokenize(text))
            medoklang_interpreter.BasicExecute(tree, env)