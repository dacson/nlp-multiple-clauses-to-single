from lark import Transformer, Tree, Token

class Graph:
    def __init__(self):
        self.G = {}

    def link(self, x, y):
        if x not in self.G: self.G[x] = [y]
        else: self.G[x] += [y]

    def show(self):
        for x in self.G:
            for y in self.G[x]:
                print(x, "==>" ,y)

class Actions(Transformer):
    def __init__(self): self.graph = Graph()
    
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
            TODO = "treat rel_clause here"
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

    def whole_sentence(self, matches):
        self.graph.show()
        return Tree("whole_sentence", matches)