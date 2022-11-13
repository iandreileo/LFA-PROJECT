from typing import Callable, Generic, TypeVar
import re
from src.REGEX import *

S = TypeVar("S")
T = TypeVar("T")

verifaux = False

class NFA(Generic[S]):
	def __init__(self):
		self.states = [] # set de stari
		self.alphabet = [] # simbolurile
		self.q0 = '' # starea initiala
		self.qf = ''  #stari finale
		self.transitions = {} # delta

	def set_states(self):
		self.states = set()
		for i in self.transitions:
			# Adaugam starea din care se pleaca
			self.states.add(i[0])

			# Adaugam starile in care se ajunge
			for j in self.transitions[i]:
				self.states.add(j)
		self.states = list(self.states)

	def set_alphabet(self):
		self.alphabet = set()
		for i in self.transitions:
			if i[1] != 'ε':
				self.alphabet.add(i[1])

	def map(self, f: Callable[[S], T]) -> 'NFA[T]':
		pass

	def next(self, from_state: S, on_chr: str) -> 'set[S]':
		if self.isFinal(from_state) or from_state not in self.states:
			return None

		if(self.transitions).__contains__((from_state, on_chr)):
			if(self.transitions).__contains__((from_state, "ε")):
				return list(set((self.transitions[from_state, on_chr] + self.transitions[from_state, "ε"])))
			else:
				return self.transitions[from_state, on_chr]
		else:
			if(self.transitions).__contains__((from_state, "ε")):
				return self.transitions[from_state, "ε"]



	def getStates(self) -> 'set[S]':
		return self.states

	def verif(self, str: str, state: S):

		# print(str, state)
		if(state == self.qf and len(str) == 0):
			global verifaux
			verifaux = True
			# return True

		if(len(str) > 0):
			future_states = self.next(state, str[0])
			if future_states != None:
				for s in future_states:
					# Testez daca e epsilon ca sa nu il consum
					# Daca sunt pe epsilon trimit tot
					if (self.transitions).__contains__((state, "ε")):
						if self.transitions[state, 'ε'] == future_states:
							self.verif(str, s)
						else:
							self.verif(str[1:], s)
					else:
							self.verif(str[1:], s)

		else:

			if (self.transitions).__contains__((state, "ε")):
				future_states = self.next(state, "")

				for s in future_states:
					self.verif(str, s)



	def accepts(self, str: str) -> bool:
		global verifaux
		verifaux = False
				
		# print(self.verif(str,self.q0))
		self.verif(str, self.q0)

		# print(verifaux)

		return verifaux

	def isFinal(self, state: S) -> bool:
		return state == self.qf

	@staticmethod
	def fromPrenex(str: str) -> 'NFA[int]':
		regex = REGEX(str)
		regex.parse()

		nfa = createFinalNFA(regex.print())

		return nfa

	def show_NFA(self):
		print(self.states)
		print(self.alphabet)
		print(self.q0)
		print(self.qf)
		print(self.transitions)

	def prelucreazaNFA_1(self, NFA_1):
		# Prelucram primul NFA
		# Decalam toate starile cu 1
		for i in range(len(NFA_1.states)):
			NFA_1.states[i] = NFA_1.states[i] + 1
		NFA_1.q0 = NFA_1.q0 + 1
		NFA_1.qf = NFA_1.qf + 1

		# Decalam toate tranzitiile cu 1
		newTransitions = {}
		for i in NFA_1.transitions:
			copieTrasitionsI = []
			# iterator = 0
			for j in NFA_1.transitions[i]:
				# print(iterator)
				copieTrasitionsI.append(j+1)
				# iterator = iterator + 1
			newTransitions[i[0] + 1, i[1]] = copieTrasitionsI
		NFA_1.transitions = newTransitions

	def prelucreazaNFA_2(self, NFA_1, NFA_2):
		# Prelucram al doilea NFA
		# Decalam toate starile cu 1
		for i in range(len(NFA_2.states)):
			NFA_2.states[i] = NFA_2.states[i] + len(NFA_1.states) + 1
		NFA_2.q0 = NFA_2.q0 + len(NFA_1.states) + 1
		NFA_2.qf = NFA_2.qf + len(NFA_1.states) + 1

		# Decalam toate tranzitiile cu 1
		newTransitions = {}
		for i in NFA_2.transitions:
			copieTrasitionsI = []
			# iterator = 0
			for j in NFA_2.transitions[i]:
				# print(iterator)
				copieTrasitionsI.append(j + len(NFA_1.states) + 1)
				# iterator = iterator + 1
			newTransitions[i[0] + len(NFA_1.states) + 1, i[1]] = copieTrasitionsI
		NFA_2.transitions = newTransitions

class UNION(NFA):
	def __init__(self, NFA_1, NFA_2):

		self.prelucreazaNFA_1(NFA_1)
		self.prelucreazaNFA_2(NFA_1, NFA_2)
	
		# Le unim
		self.q0 = 0
		self.qf = NFA_2.states[len(NFA_2.states) - 1] + 1
		self.transitions = {**NFA_1.transitions, **NFA_2.transitions}
				
		self.transitions[self.q0, 'ε'] = [NFA_1.q0, NFA_2.q0]
		self.transitions[NFA_1.qf, 'ε'] = [self.qf]
		self.transitions[NFA_2.qf, 'ε'] = [self.qf]

		self.set_alphabet()
		self.set_states()

class STAR(NFA):
	def __init__(self, NFA):
		self.q0 = 0

		# Decalez toate starile cu 1
		self.prelucreazaNFA_1(NFA)

		# starea finala
		self.qf = NFA.qf + 1

		self.transitions = NFA.transitions
		self.transitions[self.q0, 'ε'] = [NFA.q0, self.qf]
		self.transitions[NFA.qf, 'ε'] = [self.qf, NFA.q0]

		self.set_alphabet()
		self.set_states()

class CONCAT(NFA):
	def __init__(self, NFA_1, NFA_2):

		# self.prelucreazaNFA_1(NFA_1)
		self.prelucreazaNFA_CONCAT(NFA_1, NFA_2)

		self.q0 = NFA_1.q0
		self.qf = NFA_2.qf

		self.transitions = {**NFA_1.transitions, **NFA_2.transitions}
		self.transitions[NFA_1.qf, 'ε'] = [NFA_2.q0]

		self.set_alphabet()
		self.set_states()

	def prelucreazaNFA_CONCAT(self, NFA_1, NFA_2):
		# Prelucram al doilea NFA
		# Decalam toate starile cu 1
		for i in range(len(NFA_2.states)):
			NFA_2.states[i] = NFA_2.states[i] + len(NFA_1.states) + 1
		NFA_2.q0 = NFA_2.q0 + len(NFA_1.states)
		NFA_2.qf = NFA_2.qf + len(NFA_1.states)

		# Decalam toate tranzitiile cu 1
		newTransitions = {}
		for i in NFA_2.transitions:
			copieTrasitionsI = []
			# iterator = 0
			for j in NFA_2.transitions[i]:
				# print(iterator)
				copieTrasitionsI.append(j + len(NFA_1.states))
				# iterator = iterator + 1
			newTransitions[i[0] + len(NFA_1.states), i[1]] = copieTrasitionsI
		NFA_2.transitions = newTransitions


class CHAR(NFA):
	def __init__(self, char):
		self.q0 = 0
		self.qf = 1
		self.transitions = {}
		self.transitions[self.q0,char] = [self.qf]

		self.set_alphabet()
		self.set_states()

class PLUS(NFA):
	def __init__(self, NFA):
		self.q0 = 0

		# Decalez toate starile cu 1
		self.prelucreazaNFA_1(NFA)

		# starea finala
		self.qf = NFA.qf + 1

		self.transitions = NFA.transitions
		self.transitions[self.q0, 'ε'] = [NFA.q0]
		self.transitions[NFA.qf, 'ε'] = [self.qf, NFA.q0]

		self.set_alphabet()
		self.set_states()

def createFinalNFA(postfix):
	# print(postfix)
	if postfix == "''":
		postfix = " "
	stack = []
	operations = list(set(re.sub('[^A-Z]+', '', postfix)))
	keys = list(re.sub('[^a-z0-9] +', '', postfix))

	current = ""
	for i in postfix:
		if i in operations:
			current += i
			if isoperation(current):
				stack.append(current)
				current = ""
		elif i not in ['(', ')', ',']:
			if i in keys:
				stack.append(i)
				current = ""

	secondaryStack = []
	while stack:
		current = stack.pop()
		if current in keys:
			secondaryStack.append(CHAR(current))
		elif current == "STAR":
			currentNFA = secondaryStack.pop()
			newNFA = STAR(currentNFA)
			secondaryStack.append(newNFA)
		elif current == "PLUS":
			currentNFA = secondaryStack.pop()
			newNFA = PLUS(currentNFA)
			secondaryStack.append(newNFA)			   
		elif current == "UNION":
			currentNFA_1 = secondaryStack.pop()
			currentNFA_2 = secondaryStack.pop()
			newNFA = UNION(currentNFA_1, currentNFA_2)
			secondaryStack.append(newNFA)
		elif current == "CONCAT":
			currentNFA_1 = secondaryStack.pop()
			currentNFA_2 = secondaryStack.pop()
			newNFA = CONCAT(currentNFA_1, currentNFA_2)
			secondaryStack.append(newNFA)
		
	return secondaryStack[0]