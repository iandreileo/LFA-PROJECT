from NFA import *
from REGEX import REGEX


# Pasul 1 -> Formam Regex
test = REGEX("UNION a b")
test.parse()
print(test.print())

nfa = createFinalNFA(test.print())
nfa.show_NFA()

# Pasul 2 -> Regex to NFA