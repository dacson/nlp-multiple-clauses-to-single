import csv
from lark.lexer import Lexer, Token

class EnglishLexer(Lexer):
    def __init__(self, lexer_conf):
        super().__init__();
        self.f = open('dictionary.csv', 'r')
        self.csvr = csv.reader(self.f, delimiter=":")

    def load_words_from_data(self, data):
        tmp = data.split(' ')
        words = list();
        for w in tmp:
            if w[-1:] == '.': words += [w[0:-1], "."]
            elif w[-1:] == ',': words += [w[0:-1], ","]
            else: words += [w]
        return words

    def lex(self, data):
        for word in self.load_words_from_data(data):
            self.f.seek(0);
            found = False
            for token, value in self.csvr:
                if word == value:
                    found = True;
                    yield Token(token, value)
                    break
            if not found: raise TypeError(word);
            