from lark import Lark
from lexer import EnglishLexer

with open('./grammar.lark', 'r') as f: grammar = f.read();

nlp_parser = Lark(grammar, parser='lalr', lexer=EnglishLexer);

sentences = [
    "the boy whom I met yesterday cried and laughed.",
    "the big sad dog eat."
]

for s in sentences:
    print("Parsing \"" + s + "\"")
    print("--------------------------------")
    print(nlp_parser.parse(s).pretty())