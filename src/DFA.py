from typing import Callable, Generic, TypeVar

S = TypeVar("S")
T = TypeVar("T")

class DFA(Generic[S]):
	def map(self, f: Callable[[S], T]) -> 'DFA[T]':
		pass

	def next(self, from_state: S, on_chr: str) -> S:
		pass

	def getStates(self) -> 'set[S]':
		pass

	def accepts(self, str: str) -> bool:
		pass

	def isFinal(self, state: S) -> bool:
		pass

	@staticmethod
	def fromPrenex(str: str) -> 'DFA[int]':
		pass

