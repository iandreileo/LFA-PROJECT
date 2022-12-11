from __future__ import annotations
from builtins import print
from typing import Type
import codecs
import string

stack = []

def prenextree_to_string(regex, prenex):
    print(regex, prenex)
    if regex is not None:
        if regex.type in ["STAR", "PLUS"]:
            prenex.append(regex.type)
            prenextree_to_string(regex.subexpr, prenex)
        elif regex.type in ["CONCAT", "UNION"]:
            prenex.append(regex.type)
            prenextree_to_string(regex.left, prenex)
            prenextree_to_string(regex.right, prenex)
        elif regex.type == "PARAN":
            prenextree_to_string(regex.subexpr, prenex)
        elif regex.type == "ATOM":
            prenex.append(regex.symbol)

class Node:
    def __init__(self, type):
        self.type = type
        self.completed = False

    def addtostack(self):
        # if not stack:
        #     sys.stderr.write("EMPTY STACK!")
        #     return

        global stack

        top = stack.pop()
        if top.completed == True:
            self.subexpr = top
            self.completed = True
            stack.append(self)

class ParanNode(Node):
    def __init__(self):
        super().__init__("OP")
        global stack
        stack.append(self)

class ClosedParanNode(Node):
    def __init__(self):
        super().__init__("PARAN")
        global stack
        self.subexpr = None
        self.completed = True
        self.addtostack()

    def addtostack(self):
        # if not stack:
        #     sys.stderr.write("EMPTY STACK!")
        #     return
        global stack
        ultim = None
        while stack:
            penultim = stack.pop()
            if penultim.type == "OP":
                break
            if penultim.completed:
                ultim = penultim
            else:
                penultim.right = ultim
                penultim.completed = True
                ultim = penultim

        self.subexpr = ultim
        stack.append(self)

class ConcatNode(Node):
    def __init__(self):
        super().__init__("CONCAT")
        self.left = None
        self.right = None
        self.addtostack()

    # The top of the stack will be the left of the concatenation
    def addtostack(self):
        # if not stack:
        #     sys.stderr.write("EMPTY STACK!")
        #     return
        global stack
        top = stack.pop()
        if top.completed == True:
            self.left = top
            stack.append(self)

class ReunionNode(Node):
    def __init__(self):
        super().__init__("UNION")
        self.left = None
        self.right = None
        self.addtostack()

    # Merge elements on the stack until it encountering an open paranthesis
    def addtostack(self):
        # if not stack:
        #     sys.stderr.write("EMPTY STACK!")
        #     return

        global stack
        ultim = None
        while stack:
            penultim = stack.pop()
            if penultim.type == "OP":
                stack.append(penultim)
                break
            if penultim.completed:
                ultim = penultim
            else:
                penultim.right = ultim
                penultim.completed = True
                ultim = penultim

        self.left = ultim
        stack.append(self)

class SingleOpNode(Node):
    def __init__(self, type):
        super().__init__(type)
        global stack
        self.subexpr = None
        super().addtostack()

class AtomNode(Node):
    def __init__(self, symbol):
        super().__init__("ATOM")
        global stack
        self.symbol = symbol
        self.completed = True
        stack.append(self)

def generate_09():
    global stack
    ParanNode()

    for i in range(9):
        AtomNode(str(i))

        ReunionNode()

    AtomNode('9')
    ClosedParanNode()


def generateaz():
    global stack
    ParanNode()
    for i in (list(string.ascii_lowercase).remove("z")):
        AtomNode(i)
        ConcatNode()

    AtomNode('9')

    ClosedParanNode()
    



def create_prenex_string(regex):
    regex = codecs.decode(regex, 'unicode_escape')

    i = 0
    regex_len = len(regex)

    global stack
    ParanNode()
    # Parcurgem regexul

    while (i < regex_len):
        # Extragem caracterul curent
        current = regex[i]
        # print(current)

        match current:
            case "(":
                if stack[-1].completed == True:
                    ConcatNode()
                ParanNode()
            case ")":
                ClosedParanNode()
            case "|":
                ReunionNode()
            case "*":
                SingleOpNode("STAR")
            case "+":
                SingleOpNode("PLUS")
            case "\'":
                if stack[-1].completed == True:
                    ConcatNode()
                AtomNode(regex[i + 1])
                i += 3
                continue
            case "[":
                if stack[-1].completed == True:
                    ConcatNode()
                if regex[i + 1]:
                    generate_09()
                else:
                    generateaz()
                i += 5
                continue 
            case "_":
                if stack[-1].completed == True:
                    ConcatNode()
                AtomNode(current)  
        
        i += 1

    print(stack)    
    ClosedParanNode()
    print(stack)

    prenex = []
    prenextree_to_string(stack[-1], prenex)
    return prenex

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
        return (' '.join(create_prenex_string(s)))
        # pass
