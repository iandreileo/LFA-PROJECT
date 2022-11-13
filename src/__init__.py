from NFA import *
from REGEX import REGEX


# # Pasul 1 -> Formam Regex
# test = NFA.fromPrenex("ε").show_NFA()
test1 = NFA.fromPrenex("' '").accepts("")
print(test1)
# nfa = NFA.fromPrenex("CONCAT a b").accepts("ba")
# print(nfa)
# # print(nfa.next(0 , 'ε'))
# # print(nfa.isFinal(3))
# # print(nfa.getStates())
# # nfa.accepts("ba")

# # Pasul 2 -> Regex to NFA
