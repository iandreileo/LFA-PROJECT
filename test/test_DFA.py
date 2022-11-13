from typing import Callable
import unittest
from src.DFA import DFA


class DFATests(unittest.TestCase):
	def test_dfa_from_eps(self):
		self.assertTrue(DFA.fromPrenex("eps").accepts(""))
		print("eps (2p)")

	def test_dfa_from_space(self):
		self.assertTrue(DFA.fromPrenex("' '").accepts(" "))
		self.assertFalse(DFA.fromPrenex("' '").accepts(""))
		print("space (2p)")

	def test_dfa_from_void(self):
		self.assertFalse(DFA.fromPrenex("void").accepts(""))
		print("void (2p)")

	def test_dfa_from_char(self):
		self.assertTrue(DFA.fromPrenex("a").accepts("a"))
		self.assertFalse(DFA.fromPrenex("a").accepts("b"))
		print("character (2p)")

	def test_dfa_from_weird_characters(self):
		characters = "$@*	({\"'\r\n\0"
		for c in characters:
			self.assertTrue(DFA.fromPrenex("'" + c + "'").accepts(c))
		print("character (2p)")


	def test_dfa_from_concat(self):
		expr = "CONCAT a b"
		self.assertTrue(DFA.fromPrenex(expr).accepts("ab"))
		self.assertFalse(DFA.fromPrenex(expr).accepts("aba"))
		self.assertFalse(DFA.fromPrenex(expr).accepts("ba"))
		print("concat (2p)")

	def test_dfa_from_union(self):
		expr = "UNION a b"
		self.assertTrue(DFA.fromPrenex(expr).accepts("a"))
		self.assertTrue(DFA.fromPrenex(expr).accepts("b"))
		self.assertFalse(DFA.fromPrenex(expr).accepts("ab"))
		self.assertFalse(DFA.fromPrenex(expr).accepts("ba"))
		print("union (2p)")

	def test_dfa_from_star(self):
		expr = "STAR a"
		self.assertTrue(DFA.fromPrenex(expr).accepts(""))
		self.assertTrue(DFA.fromPrenex(expr).accepts("a"))
		self.assertTrue(DFA.fromPrenex(expr).accepts("aaaaaaaaaaa"))
		self.assertFalse(DFA.fromPrenex(expr).accepts("aaaaabaaaaa"))
		print("star (2p)")

	def test_dfa_from_complex_expression1(self):
		expr = "STAR UNION a b"
		self.assertTrue(DFA.fromPrenex(expr).accepts("aaababaaabaaaaa"))
		self.assertTrue(DFA.fromPrenex(expr).accepts("aaaaaaaaaa"))
		self.assertTrue(DFA.fromPrenex(expr).accepts("bbbbbbbbbbb"))
		self.assertFalse(DFA.fromPrenex(expr).accepts("baaabbbabaacabbbaaabbb"))
		print("complex 1 (30p)")

	def test_dfa_from_complex_expression2(self):
		expr = "STAR CONCAT a b"
		self.assertTrue(DFA.fromPrenex(expr).accepts("ababababab"))
		self.assertFalse(DFA.fromPrenex(expr).accepts("abababababa"))
		self.assertFalse(DFA.fromPrenex(expr).accepts("abababaabab"))
		print("complex 2 (30p)")

	def test_dfa_from_complex_expression3(self):
		expr = "STAR CONCAT a b"
		self.assertTrue(DFA.fromPrenex(expr).accepts("ababababab"))
		self.assertFalse(DFA.fromPrenex(expr).accepts("abababababa"))
		self.assertFalse(DFA.fromPrenex(expr).accepts("abababaabab"))
		print("complex 3 (30p)")

	def test_dfa_from_complex_expression4(self):
		expr = "CONCAT UNION b STAR a STAR c"
		self.assertTrue(DFA.fromPrenex(expr).accepts("aaaaaaaaaccccc"))
		self.assertTrue(DFA.fromPrenex(expr).accepts("bccccccccc"))
		self.assertFalse(DFA.fromPrenex(expr).accepts("bbbbccccccccc"))
		print("complex 4 (30p)")

	def test_dfa_from_complex_expression5(self):
		expr = "CONCAT a STAR a"
		self.assertTrue(DFA.fromPrenex(expr).accepts("aaa"))
		self.assertFalse(DFA.fromPrenex(expr).accepts(""))
		print("complex 1 (30p)")


	def test_dfa_map1(self):
		regexes = [
			("CONCAT UNION b STAR a STAR c", "abc"),
			("CONCAT a STAR a", "a"),
			("CONCAT a UNION b STAR CONCAT c d", "abcd")
		]
		for regex, alphabet in regexes:
			dfa = DFA.fromPrenex(regex)


			f : Callable[[int], int] = lambda x : x + 2

			mapped_dfa = dfa.map(f)


			states = dfa.getStates()
			newStates = mapped_dfa.getStates()

			# check if the new set of states is the result of mapping f on the old set
			self.assertSetEqual(set(map(f, states)), newStates)

			for s in states:
				# check if the same applies to the set of final states
				self.assertEqual(dfa.isFinal(s), mapped_dfa.isFinal(f(s)))

			# check if f(old_delta(old_state,c)) = new_delta(new_state, c) for each state-character pair
			for c in alphabet:
				for s in states:
					originalNext = dfa.next(s, c)
					mappedNext = mapped_dfa.next(f(s), c)

					self.assertEqual(f(originalNext), mappedNext)

