# from NFA import *
# from DFA import *
# from REGEX import REGEX

# characters = "$@*	({\"'\r\n\0"
# for c in characters:
#     print("=====================")
#     test = NFA.fromPrenex("'" + c + "'").show_NFA()
#     print("=====================")


# # # # Pasul 1 -> Formam Regex
# # test = NFA.fromPrenex("STAR CONCAT a b").show_NFA()
# # # test1 = NFA.fromPrenex("' '").accepts(" ")
# # # print(test1)
# # # nfa = NFA.fromPrenex("CONCAT a b").accepts("ba")
# # # print(nfa)
# # # # print(nfa.next(0 , 'ε'))
# # # # print(nfa.isFinal(3))
# # # # print(nfa.getStates())
# # # # nfa.accepts("ba")

# # # # Pasul 2 -> Regex to NFA
# # dfa = DFA.fromPrenex("CONCAT a b").accepts("ba")
# # print(dfa)