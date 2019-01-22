from lark import Lark, Transformer, v_args
from queue import Queue

f = open('./grammar.lark', 'r');
grammar = f.read();
f.close();

@v_args(inline=True)    # Affects the signatures of the methods
class MultipleClauseTransformer(Transformer):
    def __init__(self):
        self.nps = []
        self.vps = []
    def start(self, x): return x;
    
    def to_string(self, array):
        return array if isinstance(array, str) else " ".join(filter(lambda x: x is not None, array));
    
    def concat(self, *args):
        return self.to_string(args);
    
    def np(self, *identified):
        return self.to_string(identified);
    
    def vp(self, *identified):
        return self.to_string(identified);

    def sentence(self, noun, verb):
        return noun + " " + verb + ".";

    def thrd_prsn_conjuagated_verb(self, verb):
        return verb + "s";

    def ing_conjugated_verb(self, be, verb):
        return be + " " + verb + "ing";

nlp_parser = Lark(grammar, parser='lalr', transformer=MultipleClauseTransformer());

result = nlp_parser.parse("a big sad dog did not eat or killed the cat nor the man.");

print(result);
