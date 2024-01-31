from state import *
import regex
import copy


# NFA is a class with four fields:
# -states = a list of states in the NFA
#  Note that the start state is always state 0
# -accepting = A dictionary, the key is the state id 
#  and value is a boolean indicating which states are accepting
# -alphabet = a list of symbols in the alphabet of the regular language.
#  Note that & can not be included because we use it as epsilon
# -startS = it is the start state id which we assume it is always 0

class NFA:
    def __init__(self):
        self.states = []
        self.is_accepting = dict()
        self.alphabet = ['&']
        self.startS = 0
        pass

    def __str__(self):
        pass

    # You should write this function.
    # It takes two states and a symbol. It adds a transition from 
    # the first state of the NFA to the other input state of the NFA.
    def addTransition(self, s1, s2, sym='&'):
        if sym in s1.transition:
            s1.transition[sym].add(s2)
        else:
            s1.transition[sym] = {s2}

    # You should write this function.
    # It takes a nfa, adds all the states from that nfa and return a
    # mapping of (state number in old NFA to state number in this NFA) as a dictionary.
    def addStatesFrom(self, nfa):
        self.alphabet = set(self.alphabet).union(set(nfa.alphabet))
        old_state_num = len(self.states)
        for state in nfa.states:
            temp = state.id
            state.id += old_state_num
            self.states.append(state)
            self.is_accepting[state.id] = nfa.is_accepting[temp]

    # You should write this function.
    # It takes a state and returns the epsilon closure of that state 
    # which is a set of states which are reachable from this state 
    # on epsilon transitions.
    def epsilonClose(self, ns):
        states = []
        queue = [ns]
        visited = set()
        while queue:
            curr = queue.pop(0)
            if curr in visited:
                continue
            else:
                for sym, nn in self.states[curr.id].transition.items():
                    if sym == '&':
                        for s in nn:
                            states.append(s)
                            queue.append(s)
            visited.add(curr)
        return states

    # It takes a string and returns True if the string is in the language of this NFA
    def isStringInLanguage(self, string):
        str_end = len(string)
        queue = [(self.states[0], 0)]
        visited = set()
        while queue:
            curr_state, pos = queue.pop(0)
            if pos == str_end:
                if curr_state.id in self.is_accepting and self.is_accepting[curr_state.id]:
                    return True
                for n in self.epsilonClose(curr_state):
                    if (n, pos) not in visited:
                        queue.append((n, pos))
                        visited.add((n, pos))
                continue

            if string[pos] in curr_state.transition:
                next_states = curr_state.transition[string[pos]]
                for next_state in next_states:
                    if (next_state, pos + 1) not in visited:
                        queue.append((next_state, pos + 1))
                        visited.add((next_state, pos + 1))
            for n in self.epsilonClose(curr_state):
                if (n, pos) not in visited:
                    queue.append((n, pos))
                    visited.add((n, pos))
        return False

