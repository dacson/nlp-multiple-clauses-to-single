from lark import Lark
from lexer import EnglishLexer
from transformer import Actions

with open('./grammar.lark', 'r') as f: grammar = f.read();

sentences = [
    # "the boy whom I met yesterday cried and laughed.",
    "the boy who is tall, skinny and strange smile and laugh.",
    "he can speak italian and english.",
    "the dog eat a man who is tall."
]

for s in sentences:
    nlp_parser = Lark(grammar, parser='lalr', lexer=EnglishLexer, transformer=Actions() );
    print("Parsing \"" + s + "\"")
    print("--------------------------------")
    print(nlp_parser.parse(s).pretty())
