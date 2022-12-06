from __future__ import annotations
from builtins import print
from typing import Type
import codecs

# from Regex import Character, Operator

class RegexElement:
    def __init__(self, type):
        self.type = type
        self.is_complete = False

    # The top of the stack will be the subexp
    def addtostack(self, stack):
        if not stack:
            sys.stderr.write("EMPTY STACK!")
            return

        top = stack.pop()
        if top.is_complete:
            self.subexpr = top
            self.is_complete = True
            stack.append(self)


class Concatenation(RegexElement):
    def __init__(self, stack):
        super().__init__("CONCAT")
        self.left = None
        self.right = None
        self.addtostack(stack)

    # The top of the stack will be the left of the concatenation
    def addtostack(self, stack):
        if not stack:
            sys.stderr.write("EMPTY STACK!")
            return

        top = stack.pop()
        if top.is_complete:
            self.left = top
            stack.append(self)

    
class Reunion(RegexElement):
    def __init__(self, stack):
        super().__init__("UNION")
        self.left = None
        self.right = None
        self.addtostack(stack)

    # Merge elements on the stack until it encountering an open paranthesis
    def addtostack(self, stack):
        if not stack:
            sys.stderr.write("EMPTY STACK!")
            return

        ultim = None
        while stack:
            penultim = stack.pop()
            if penultim.type == "OP":
                stack.append(penultim)
                break
            if penultim.is_complete:
                ultim = penultim
            else:
                penultim.right = ultim
                penultim.is_complete = True
                ultim = penultim

        self.left = ultim
        stack.append(self)


class Star(RegexElement):
    def __init__(self, stack):
        super().__init__("STAR")
        self.subexpr = None
        super().addtostack(stack)


class Plus(RegexElement):
    def __init__(self, stack):
        super().__init__("PLUS")
        self.subexpr = None
        super().addtostack(stack)


class OpenParan(RegexElement):
    def __init__(self, stack):
        super().__init__("OP")
        stack.append(self)


class CloseParan(RegexElement):
    def __init__(self, stack):
        super().__init__("PARAN")
        self.subexpr = None
        self.is_complete = True
        self.addtostack(stack)

    # Merge elements on the stack until encountering an open paranthesis 
    # (removes the paranthesis)
    def addtostack(self, stack):
        if not stack:
            sys.stderr.write("EMPTY STACK!")
            return

        ultim = None
        while stack:
            penultim = stack.pop()
            if penultim.type == "OP":
                break
            if penultim.is_complete:
                ultim = penultim
            else:
                penultim.right = ultim
                penultim.is_complete = True
                ultim = penultim

        self.subexpr = ultim
        stack.append(self)


class Atom(RegexElement):
    def __init__(self, symbol, stack):
        super().__init__("ATOM")
        self.symbol = symbol
        self.is_complete = True
        stack.append(self)


# Push the expression "a | b | c ... | z" on stack
def any_alpha(stack):
    OpenParan(stack)
    for i in range(97, 122):
        Atom(chr(i), stack)
        Concatenation(stack)
    Atom('z', stack)
    CloseParan(stack)

# Push the expression "0 | 1 | 2 | ... | 9" on stack
def any_digit(stack):
    OpenParan(stack)
    for i in range(9):
        Atom(str(i), stack)
        Reunion(stack)
    Atom('9', stack)
    CloseParan(stack)

# Create a list of strings representing the regex in prenex form.
# Execute a preorder traversal of the AST
def prenextree_to_string(regex, prenex):
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

# Create the AST and return a the regex in prenex form as a list of strings
def create_prenex_string(regex):
    regex = codecs.decode(regex, 'unicode_escape')
    i = 0
    stack = []
    OpenParan(stack)

    while(i < len(regex)):
        c = regex[i]
        if c == '|':
            Reunion(stack)
        elif c == '*':
            Star(stack)
        elif c == '+':
            Plus(stack)
        elif c == '(':
            if stack[-1].is_complete:
                Concatenation(stack)
            OpenParan(stack)
        elif c == ')':
            CloseParan(stack)
        elif c == '\'':
            if stack[-1].is_complete:
                Concatenation(stack)
            Atom(regex[i + 1], stack)
            i += 3
            continue
        elif c == '[':
            if stack[-1].is_complete:
                Concatenation(stack)
            if regex[i + 1] == '0':
                any_digit(stack)
            else:
                any_alpha(stack)
            i += 5
            continue
        else:
            if stack[-1].is_complete:
                Concatenation(stack)
            Atom(c, stack)

        i += 1

    CloseParan(stack)

    prenex = []
    # print(stack[-1])
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
