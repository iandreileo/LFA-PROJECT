# from Regex import *
# from Parser import *
# from DFA import *

# # # # s = "\' \'\'a\'"
# # # # s = Parser.toPrenex(s)
# # # # print(s)
# # # # test1 = DFA.fromPrenex(s).accepts(" a")

# # # s = "\'\n\'a\'\t\'b"
# # # test5 = Parser.toPrenex(s)
# # # print(DFA.fromPrenex(s).accepts("\na\tb")
# # # print(test5)


# # # # test2 = DFA.fromPrenex(s).accepts("@a")
# # # # print("escaped chars 1 (1p)")

# # s = "a|(b|(c|de))"
# #         #self.assertEqual(Parser.toPrenex(s), "UNION a UNION b UNION c CONCAT d e")
# # s = Parser.toPrenex(s)
# # print(s)

# # s = "[A-Z]"
# # s = "a|(b|(c|de))"
# s = "eps"
# s = Parser.toPrenex(s)
# print(s)
# DFA.fromPrenex(s).accepts("K")
# # self.assertTrue(DFA.fromPrenex(s).accepts("K"))
# # self.assertTrue(DFA.fromPrenex(s).accepts("T"))
# # self.assertTrue(DFA.fromPrenex(s).accepts("U"))