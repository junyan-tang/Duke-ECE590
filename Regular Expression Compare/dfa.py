import copy
from state import *


# DFA is a class with four fields:
# -states = a list of states in the DFA
#  Note that the start state is always state 0
# -accepting = A dictionary, the key is the state id 
#  and value is a boolean indicating which states are accepting
# -alphabet = a list of symbols in the alphabet of the regular language.
#  Note that & can not be included because we use it as epsilon
# -startS = it is the start state id which we assume it is always 0
class DFA:
    def __init__(self):
        self.states = []
        self.is_accepting = dict()
        self.alphabet = []
        self.startS = 0
        pass

    def __str__(self):
        pass
        # You should write this function.

    # It takes two states and a symbol/char. It adds a transition from
    # the first state of the DFA to the other input state of the DFA.
    def addTransition(self, s1, s2, sym):
        s1.transition[sym] = {s2}

    # It returns a DFA that is the complement of this DFA
    def complement(self):
        for i in self.is_accepting.keys():
            self.is_accepting[i] = False if self.is_accepting[i] else True

    # You should write this function.
    # It takes a string and returns True if the string is in the language of this DFA
    def isStringInLanguage(self, string):
        curr = 0
        for i in string:
            if i not in self.states[curr].transition:
                return False
            else:
                curr = list(self.states[curr].transition[i])[0].id
        return self.is_accepting[curr]

    # You should write this function.
    # It runs BFS on this DFA and returns the shortest string accepted by it
    def shortestString(self):
        queue_id = [0]
        queue_info = [""]
        visited = set()

        while queue_id:
            curr_id = queue_id.pop(0)
            curr_info = queue_info.pop(0)
            if self.is_accepting[curr_id]:
                return curr_info
            if curr_id not in visited:
                visited.add(curr_id)
                for sym, ss in self.states[curr_id].transition.items():
                    for s in ss:
                        queue_id.append(s.id)
                        queue_info.append(curr_info + sym)

        return ""
