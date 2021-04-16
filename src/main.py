'''
Made by IMightBeMe and IMayBeMe on replit.com.

Source code is available on github at https://github.com/IMightBeMe/Scythe and replit at https://replit.com/@IMightBeMe/Scythe?v=1
'''

from scythe_lexer import SLexer
from scythe_parser import SParser
from scythe_execute import SExecute


if __name__ == '__main__':
    lexer = SLexer()
    parser = SParser()
    names = {}

    scythe_file = open('src/main.sy', 'r')

    lines = scythe_file.readlines()
    for i in lines:
        if i:
            tree = parser.parse(lexer.tokenize(i))
            SExecute(tree, names)
