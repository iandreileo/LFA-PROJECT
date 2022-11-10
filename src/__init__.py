from NFA import *
from REGEX import REGEX


# Pasul 1 -> Formam Regex
test = NFA.fromPrenex("UNION a b").show_NFA()
nfa = NFA.fromPrenex("UNION a b")
# print(nfa.next(0 , 'ε'))
# print(nfa.isFinal(3))
# print(nfa.getStates())
nfa.accepts("b")

# Pasul 2 -> Regex to NFA
