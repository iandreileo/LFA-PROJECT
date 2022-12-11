import unittest
from src.Parser import Parser
from src.DFA import DFA

class RegexParseTests(unittest.TestCase):
    maxDiff = None
    def test_escaped_chars_1(self):
        s = "\' \'\'a\'"
        # self.assertEqual(Parser.toPrenex(s), "CONCAT @ a")
        s = Parser.toPrenex(s)
        self.assertTrue(DFA.fromPrenex(s).accepts(" a"))
        self.assertFalse(DFA.fromPrenex(s).accepts("@a"))
        print("escaped chars 1 (1p)")