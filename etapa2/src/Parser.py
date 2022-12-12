from __future__ import annotations
import codecs
import string

# Definim stack-ul global
stack = []

# Defininim clasa standard de nod
class Node:
    def __init__(self, type):
        self.type = type
        self.completed = False

    # Functia de adauga in stiva
    # Care pune in varful stivei expresia
    def stack_append(self):
        global stack
        top = stack.pop()
        if top.completed == True:
            self.subexpr = top
            self.completed = True
            stack.append(self)


# Tipul de nod corespunzator operatiei de concatenare
# Care mosteneste Node
# Are 2 membrii - stang si drept
class ConcatNode(Node):
    def __init__(self):
        global stack
        super().__init__("CONCAT")
        self.left = None
        self.right = None
        self.stack_append()

    # Functia de adaugare in stiva
    # Adaugam in varful sivei 
    # Primul parametru al concatenarii
    def stack_append(self):
        global stack

        top = stack.pop()
        if top.completed == True:
            self.left = top
            stack.append(self)


# Tipul de nod corespunzator operatiei de reuniune
# Care mosteneste Node
# Are 2 membrii - stang si drept    
class UnionNode(Node):
    def __init__(self):
        super().__init__("UNION")
        global stack
        self.left = None
        self.right = None
        self.stack_append()

    # Functia de adaugare in stiva
    # Cat timp avem posibilittea, facem reuniune pe stiva
    def stack_append(self):
        ultim = None
        global stack

        while stack:
            penultim = stack.pop()
            if penultim.type == "OP":
                stack.append(penultim)
                break
            if penultim.completed == True:
                ultim = penultim
            else:
                penultim.right = ultim
                penultim.completed = True
                ultim = penultim

        self.left = ultim
        stack.append(self)


# Tipul de nod corespunzator operatiilor cu un singur parametru
# Star si Plus
# Care mosteneste Node
class SingleOp(Node):
    def __init__(self, type):
        super().__init__(type)
        self.subexpr = None
        super().stack_append()

# Tipul de nod corespunzator deschiderii unei operatii
# Care mosteneste Node
class OpenParan(Node):
    def __init__(self):
        super().__init__("OP")
        global stack
        stack.append(self)

# Tipul de nod corespunzator inchiderii unei operatii
# Care mosteneste Node
class CloseParan(Node):
    def __init__(self):
        super().__init__("PARAN")
        self.subexpr = None
        self.completed = True
        self.stack_append()

    def stack_append(self):
        global stack

        ultim = None
        while stack:
            penultim = stack.pop()
            if penultim.type == "OP":
                break
            if penultim.completed == True:
                ultim = penultim
            else:
                penultim.right = ultim
                penultim.completed = True
                ultim = penultim

        self.subexpr = ultim
        stack.append(self)

# Tipul de nod corespunzator unui atom
# Care mosteneste Node
class Atom(Node):
    def __init__(self, symbol):
        super().__init__("ATOM")
        self.symbol = symbol
        self.completed = True
        global stack

        stack.append(self)


# Functia prin care adaugam reuniunea dintre toate caracterele de la a-z 
# Cand intalnim [a-z]
def generateaz():
    OpenParan()
    for i in (list(string.ascii_lowercase).remove("z")):
        Atom(i)
        ConcatNode()
    Atom('z')
    CloseParan()

# Functia prin care adaugam reuniunea dintre toate numerele 0-9
# Cand intalnim [0-9]
def generate09():
    OpenParan()
    for i in range(9):
        Atom(str(i))
        UnionNode()
    Atom('9')
    CloseParan()


# Parcurgem AST-ul si formam array-ul final prenex
def parse_ast(regex, prenex):
    # Daca nodul curent are 2 parametrii
    if regex.type == "CONCAT" or regex.type == "UNION":
        # Apelam recursiv pe ambii parametrii
        prenex.append(regex.type)
        parse_ast(regex.left, prenex)
        parse_ast(regex.right, prenex)
    # Daca nodul curent are doar un parametru
    elif regex.type == "STAR" or regex.type == "PLUS":
        prenex.append(regex.type)
        # Apelam recursiv subexpresia parametrului
        parse_ast(regex.subexpr, prenex)
    # Daca nodul curent este la un inceput
    # Apelam recursiv pe subexpresia
    elif regex.type == "PARAN":
        parse_ast(regex.subexpr, prenex)
    # Daca nodul curent este atom si nu mai are nicio subexpresie
    elif regex.type == "ATOM":
        prenex.append(regex.symbol)

# Functia prin care parsam regex-ul primit si il transformam
# Intr-o forma acceptabila
def create_prenex_string(regex):
    regex = codecs.decode(regex, 'unicode_escape')
    i = 0
    global stack
    OpenParan()

    # Iteram prin regex
    while(i < len(regex)):
        # Caracterul curent
        c = regex[i]
        
        # Testam cu ce este egal caracterul curent
        # Si instantionam in node de acel tip
        if c == '(':
            if stack[-1].completed == True:
                ConcatNode()
            OpenParan()
        elif c == ')':
            CloseParan()
        elif c == '|':
            UnionNode()
        elif c == '*':
            SingleOp("STAR")
        elif c == '+':
            SingleOp("PLUS")
        elif c == '\'':
            if stack[-1].completed == True:
                ConcatNode()
            Atom(regex[i + 1])
            i += 3
            continue
        elif c == '[':
            if stack[-1].completed == True:
                ConcatNode()
            if regex[i + 1] == '0':
                generate09()
            else:
                generateaz()
            i += 5
            continue
        else:
            if stack[-1].completed == True:
                ConcatNode()
            Atom(c)

        i += 1

    CloseParan()
    
    return stack

class Parser:
    # This function should:
    # -> Classify input as either character(or string) or operator
    # -> Convert special inputs like [0-9] to their correct form
    # -> Convert escaped characters
    # You can use Character and Operator defined in Regex.py
    @staticmethod
    def preprocess(regex: str) -> list:
        # print(str)
        pass

    # This function should construct a prenex expression out of a normal one.
    @staticmethod
    def toPrenex(s: str) -> str:
        # Formam stiva AST
        create_prenex_string(s)

        # Din AST transformam in forma aceptata
        global stack
        prenex = []
        parse_ast(stack[-1], prenex)
        return ' '.join(prenex)