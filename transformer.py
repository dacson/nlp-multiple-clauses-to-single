from lark import Transformer, Tree, Token

class Actions(Transformer):
    def ap(self, matches):
        adjs = []
        for match in matches:
            if type(match) is Token:
                if match.type == "COORD": continue
                adjs += [str(match)]
            else:
                for child in match.children:
                    adjs += [str(child)]
        return Tree("AP", adjs)
    
    def ng(self, matches):
        if type(matches[-1]) is Token and matches[-1].type == "NOUN":
            return Tree("NG", [" ".join([str(x) for x in matches])])
        return Tree("NG", matches)

    def np(self, matches):
        if type(matches[-1]) is Tree and matches[-1].data == "rel_clause":
            NG, rel_clause = matches
            rel_clause_sentence = matches[-1].children[1]
            if len(rel_clause_sentence.children) == 1:
                VP = rel_clause_sentence.children[0]
                for str_verb_phrase in VP.children:
                    for str_noun_phrase in NG.children:
                        print(str_noun_phrase + " " + str_verb_phrase + ".")
                return Tree("NP", NG.children)
        return Tree("np", matches)
    
    def vp(self, matches):
        return Tree("vp", matches)
    
    def conjugated_verb(self, matches):
        return " ".join([str(x) for x in matches]);

    def single_vp(self, matches):
        if len(matches) == 2:
            svps = []
            c_verb, complement = matches
            for x in complement.children:
                svps += [str(c_verb) + " " + str(x)]
            return Tree("SINGLE_VP", svps)
        return Tree("SINGLE_VP", matches)
    
    def add_vp(self, matches):
        vp1, _, vp2 = matches
        return Tree("ADD_VP", [vp1, vp2])
    
    def vp(self, matches):
        arr = [];
        for match in matches:
            for child in match.children:
                if type(child) is Tree and child.data == "VP":
                    for grd_child in child.children:
                        arr += [grd_child]
                else:
                    arr += [child]
        return Tree("VP", arr)

    def sentence(self, matches):
        if len(matches) == 2:
            NP, VP = matches
            for noun_phrase in NP.children:
                for verb_phrase in VP.children:
                    print(noun_phrase + " " + verb_phrase + ".")
            return Tree("sentence", [])
        return Tree("sentence", matches)

    def whole_sentence(self, matches):
        return Tree("whole_sentence", [])