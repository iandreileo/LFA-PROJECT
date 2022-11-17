from typing import Callable, Generic, TypeVar
from src.NFA import *

S = TypeVar("S")
T = TypeVar("T")

class DFA(Generic[S]):
	def __init__(self, alphabet, states, q0, qf, transitions):
		self.alphabet = alphabet # alfabet
		self.states = states # stari
		self.initialstate = q0 # stare initiala
		self.finalstates = qf # stari finale
		self.transitions = transitions # tranzitii

	def map(self, f: Callable[[S], T]) -> 'DFA[T]':
		pass

	def next(self, from_state: S, on_chr: str) -> S:

		if(self.transitions).__contains__((from_state, on_chr)):
			return self.transitions[from_state, on_chr]

		return None

	def getStates(self) -> 'set[S]':
		return self.states

	# Functia care primeste o configuratie si o returneaza pe urmatoarea sau None
	def nextconfig(self, conf):
		(s1, word) = conf
		ch = word[0]
		s2 = self.next(s1, ch)
		if s2 is None:
			return None
		return s2, word[1:]

	def accepts(self, str: str) -> bool:
		state = self.initialstate
		# Parcurgem pana la sfarsit
		# Ultima stare la care ajungem o testam
		# Daca e stare finala
		while str != "":
			ret = self.nextconfig((state, str))
			if ret is None:
				return False
			state, str = ret
		return state in self.finalstates

	def isFinal(self, state: S) -> bool:
		pass

	# Testam daca o stare este sink
	def issink(self, s):
		# Testam daca starea e finala
		# Daca e finala nu e sink
		if s in self.finalstates:
			return False
		# Testam daca gasim o tranzitie
		# Care sa plece din starea data
		# Si sa ajunga in cel putin o stare inafara de ea
		if s in self.transitions:
			for key in self.transitions[s]:
				if not self.transitions[s][key] == s:
					return False
		return True

	# Functia care testeaza daca este intr o stare sink
	def testsinks(self, word):
		state = self.initialstate
		while word != "":
			ret = self.nextconfig((state, word))
			if ret is None:
				return True
			state, word = ret
		return self.issink(state)

	@staticmethod
	def fromPrenex(str: str) -> 'DFA[int]':
		nfa = NFA.fromPrenex(str)
		dfa = NFA2DFA(nfa)
		# print(dfa.show_DFA())
		return dfa

	def show_DFA(self):
		print("states: " + str(self.states))
		print("alph: " + str(self.alphabet))
		print("initial states: " + str(self.initialstate))
		print("final states: " + str(self.finalstates))
		print("transitions: " + str(self.transitions))

def NFA2DFA(nfa):
	# Calculam epsilon closures
	epsilon_closures = {}
	for i in nfa.states:
		epsilon_closures[i] = epsilon_closure(nfa,i)


	# Setam starea initiala a DFA-ului
	# Ca fiind ec pentru starea 0 din nfa
	q0 = epsilon_closures[nfa.q0]
		
	# Formam tranzitiile
	alphabet = []
	for i in nfa.alphabet:
		if i != "ε":
			alphabet.append(i)
	states = [q0]
	transitions = []

	# Parcurgem in continuare
	for i in states:
		for j in alphabet:
			current = []
			for k in i:
				if (k,j) in nfa.transitions.keys():
					for contor in nfa.transitions[k,j]:
						current.append(epsilon_closures[contor])
			# print("\n")
			if current:
				# print(current)
				allnumbers = set()
				for contor in current:
					# print("CONTOR: " + str(contor))
					allnumbers.update(contor)
				# print(allnumbers)
				if allnumbers not in states:
					states.append(allnumbers)
				transitions.append(i)
				transitions.append(j)
				transitions.append(allnumbers)

	# Setam starile finale care contin qf
	final_states = []
	for i in states:
		# print(nfa.qf, i)
		if nfa.qf in i:
			final_states.append(i)

	# transformam codurile in stari normale
	new_states = {}
	contor = 0
	for i in states:
		new_states[contor] = i
		contor = contor + 1

	# inlocuim peste tot
	contor = 0

	# Inlocuim starile
	for i in states:
		states[contor] = contor
		contor = contor + 1

	# Inlocuim tranzitiile
	new_transitions = {}
	i = 0
	while i < len(transitions):
		first_state = transitions[i]
		char = transitions[i+1]
		final_state = transitions[i+2]
		for j in new_states:
			if new_states[j] == first_state:
				first_state = j
			if new_states[j] == final_state:
				final_state = j
		new_transitions[first_state, char] = final_state
		i = i + 3

	# Inlocuim starile finale
	new_final_states = []
	for i in final_states:
		for j in new_states:
			if new_states[j] == i:
				new_final_states.append(j)

	# Testam daca avem vreun sink state de adaugat
	# Trec prin fiecare nod si testez daca am drum pe fiecare din alfabet
	sink = 0
	new_aux_state = -1
	for i in states:
		for j in alphabet:
			# print(i,j)
			if (i,j) not in new_transitions:
				# print("TREBUIE ADAUGAT")
				if sink == 0:
					new_aux_state = len(states)
					sink = 1
					for ch in alphabet:
						new_transitions[new_aux_state,ch] = new_aux_state
				new_transitions[i,j] = new_aux_state
	if new_aux_state != -1:
		states.append(new_aux_state)

	return DFA(alphabet, states, 0, new_final_states, new_transitions)

# Functie preluata din checker-ul de anul trecut pentru closure (repet materia)
def epsilon_closure(nfa, state):
	def epsilon_closure_aux(nfa, state, closure):
		for next_state in nfa.transitions.get((state, "ε"), set()):
			if next_state not in closure:
				closure |= {next_state}
				closure |= epsilon_closure_aux(nfa, next_state, closure)

		return closure

	return epsilon_closure_aux(nfa, state, {state})
