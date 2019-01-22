from lark import Lark, Transformer, v_args
from queue import Queue

grammar = """
    start: sentence"."
    sentence: np vp
    np: (DET  | ) (CARD | ) (ORD | ) (QUANT | ) (ap | ) NOUN
        | np COORD np
    ap: ADJ -> concat | ADJ ap -> concat
    vp: conjugated_verb (np | ) -> concat
        | vp COORD vp
    
    conjugated_verb: (AUXILIARY | ) (NOT | ) VERB -> concat
        | VERB"s" -> thrd_prsn_conjuagated_verb
        | (BE | ) (NOT | ) (VERB_ING | VERB_EN | ) -> concat
        | HAVE (NOT | ) (VERB_EN | ) -> concat

    COORD.2: "&"
        | "nor"
        | "or"
        | "and"
    DET: "these" | "the" | "an" | "a" | "this" | "those" | "that"
    CARD: "first" | "second"
    ORD: "two" | "three" | "four"
    QUANT: "few"
    NOUN: "dog" | "I" | "cat" | "man"

    ADJ: "big" | "sad" | "small" | "red" | "happy"

    BE: "is" | "are" | "have been" | "has been"
    HAVE: "have" | "has"
    VERB: "eat" | "smile" | "love" | "kill"
    VERB_ING: VERB"ing" | "smiling"
    VERB_ED: VERB"ed" | "knew"
    VERB_EN: VERB"ed" | "known"
    AUXILIARY: "do" | "does" | "did" | "will"
    NOT: "not" | "n't"

    %ignore " "
"""

@v_args(inline=True)    # Affects the signatures of the methods
class MultipleClauseTransformer(Transformer):
    def __init__(self):
        self.nps = []
        self.vps = []
    def start(self, x): return x;
    def to_string(self, array): return array if isinstance(array, str) else " ".join(filter(lambda x: x is not None, array));
    def concat(self, *args): return self.to_string(args);
    def np(self, *identified): return self.to_string(identified);
    def vp(self, *identified): return self.to_string(identified);
    def sentence(self, noun, verb): return noun + " " + verb + ".";
    def thrd_prsn_conjuagated_verb(self, verb): return verb + "s";
    def ing_conjugated_verb(self, be, verb): return be + " " + verb + "ing";

nlp_parser = Lark(grammar, parser='lalr', transformer=MultipleClauseTransformer());

result = nlp_parser.parse("a big sad dog did not eat or killed the cat nor the man.");

print(result);
