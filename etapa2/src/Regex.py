# from extra_functions import *

# Functia prin care testam daca o operatie este pentru un char
class o1e:
    def __init__(self, char, sign):
        self.char = char
        self.sign = sign

    def iscomplete(self):
        return self.char != "?"
    
    def __str__(self):
        return self.sign + "(" + self.char + ")"

    def getsign(self):
        return self.sign

    def setchar(self, newchar):
        self.char = newchar

    def __radd__(self, other):
        return other + str(self)

    def __add__(self, other):
        return str(self) + other


class o2e:
    def __init__(self, char1, char2, sign):
        self.char1 = char1
        self.char2 = char2
        self.sign = sign

    def iscomplete(self):
        return self.char1 != "?" and self.char2 != "?"
    
    def charoneexists(self):
        return self.char1 != "?"

    def __str__(self):
        return self.sign + "(" + self.char1 + "," + self.char2 + ")"

    def getsign(self):
        return self.sign

    def setchar(self, newchar):
        if self.char1 != "?":
            self.char2 = newchar
        else:
            self.char1 = newchar
    
    def __radd__(self, other):
        return other + str(self)

    def __add__(self, other):
        return str(self) + other


def checkIfo1e(op):
    if op == "STAR" or op == "PLUS" or op == "MAYBE":
        return True
    return False

# Functia prin care testam daca suntem pe o operatie
def isoperation(op):
    if op == "STAR" or op == "PLUS" or op == "UNION" or op == "CONCAT":
        return True
    return False



class Regex():
    def __init__(self, prenex):
        self.prenex = prenex.replace("eps", 'ε').split(" ")
        # TODO: De rezolvat testul cu acele probleme de caractere

    def parse(self):
        # Parsam prenexul
        parsedPrenex = []

        for i in self.prenex:
            if isoperation(i):
                if checkIfo1e(i):
                    # Avem o operatie cu un char
                    parsedPrenex.append(o1e("?", i))
                else:
                    # Avem o operatie cu 2 char
                    parsedPrenex.append(o2e("?", "?", i))
            else:
                # Parcurgem invers si facem append la char
                for j in reversed(parsedPrenex):
                    if checkIfo1e(j.getsign()):
                        # Avem o operatie cu un char
                        if not j.iscomplete():
                            j.setchar(i)
                            break
                    else:
                        # Avem o operatie cu 2 char
                        if not j.iscomplete():
                            j.setchar(i)
                            break
                # while aici
                while len(parsedPrenex) > 1 and parsedPrenex[-1].iscomplete():
                    current = parsedPrenex.pop()
                    parsedPrenex[-1].setchar(current)
            
        if parsedPrenex == []:
            parsedPrenex = self.prenex

        self.prenex = parsedPrenex

    def print(self):
        aux = ""
        for i in self.prenex:
            aux += i
        return aux