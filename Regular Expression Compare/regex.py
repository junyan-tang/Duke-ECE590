from nfa import *
from state import *


def nfaUnion(nfa1, nfa2):
    l_num = len(nfa1.states)
    nfa = EpsilonRegex().transformToNFA()
    nfa.is_accepting[0] = False
    nfa.addStatesFrom(nfa1)
    nfa.addStatesFrom(nfa2)
    nfa.addTransition(nfa.states[0], nfa.states[1])
    nfa.addTransition(nfa.states[0], nfa.states[l_num + 1])
    return nfa


class Regex:
    def __repr__(self):
        ans = str(type(self)) + "("
        sep = ""
        for i in self.children:
            ans = ans + sep + repr(i)
            sep = ", "
            pass
        ans = ans + ")"
        return ans

    def transformToNFA(self):
        pass

    pass


class ConcatRegex(Regex):
    def __init__(self, r1, r2):
        self.children = [r1, r2]
        pass

    def __str__(self):
        return "{}{}".format(self.children[0], self.children[1])

    def transformToNFA(self):
        nfa_l = self.children[0].transformToNFA()
        nfa_r = self.children[1].transformToNFA()
        pre_state = len(nfa_l.states)
        nfa_l.addStatesFrom(nfa_r)
        for i in range(pre_state):
            if nfa_l.is_accepting[i]:
                nfa_l.is_accepting[i] = False
                nfa_l.addTransition(nfa_l.states[i], nfa_l.states[pre_state])
        return nfa_l


class StarRegex(Regex):
    def __init__(self, r1):
        self.children = [r1]
        pass

    def __str__(self):
        return "({})*".format(self.children[0])

    def transformToNFA(self):
        nfa_l = EpsilonRegex().transformToNFA()
        nfa_r = self.children[0].transformToNFA()
        nfa_l.addStatesFrom(nfa_r)
        for i in range(len(nfa_l.states)):
            if nfa_l.is_accepting[i] and i != 1:
                nfa_l.addTransition(nfa_l.states[i], nfa_l.states[1])
        return nfa_l


class OrRegex(Regex):
    def __init__(self, r1, r2):
        self.children = [r1, r2]
        pass

    def __str__(self):
        return "(({})|({}))".format(self.children[0], self.children[1])

    def transformToNFA(self):
        nfa_l = self.children[0].transformToNFA()
        nfa_r = self.children[1].transformToNFA()
        nfa = nfaUnion(nfa_l, nfa_r)
        return nfa


class SymRegex(Regex):
    def __init__(self, sym):
        self.sym = sym
        pass

    def __str__(self):
        return self.sym

    def __repr__(self):
        return self.sym

    def transformToNFA(self):
        nfa = NFA()
        if self.sym not in nfa.alphabet:
            nfa.alphabet.append(self.sym)
        nfa.states = [State(0), State(1)]
        nfa.states[0].transition[self.sym] = {nfa.states[1]}
        nfa.is_accepting[1] = True
        nfa.is_accepting[0] = False
        return nfa


class EpsilonRegex(Regex):
    def __init__(self):
        pass

    def __str__(self):
        return '&'

    def __repr__(self):
        return '&'

    def transformToNFA(self):
        nfa = NFA()
        nfa.states = [State(0)]
        nfa.is_accepting[0] = True
        return nfa


class ReInput:
    def __init__(self, s):
        self.str = s
        self.pos = 0
        pass

    def peek(self):
        if self.pos < len(self.str):
            return self.str[self.pos]
        return None

    def get(self):
        ans = self.peek()
        self.pos += 1
        return ans

    def eat(self, c):
        ans = self.get()
        if ans != c:
            raise ValueError("Expected " + str(c) + " but found " + str(ans) +
                             " at position " + str(self.pos - 1) + " of  " + self.str)
        return c

    def unget(self):
        if self.pos > 0:
            self.pos -= 1
            pass
        pass

    pass


# R -> C rtail
# rtail -> OR C rtail | eps
# C -> S ctail
# ctail -> S ctail | eps
# S -> atom stars
# atom -> (R) | sym | &
# stars -> * stars | eps


# It gets a regular expression string and returns a Regex object.
def parse_re(s):
    inp = ReInput(s)

    def parseR():
        return rtail(parseC())

    def parseC():
        return ctail(parseS())

    def parseS():
        return stars(parseA())

    def parseA():
        c = inp.get()
        if c == '(':
            ans = parseR()
            inp.eat(')')
            return ans
        if c == '&':
            return EpsilonRegex()
        if c in ')|*':
            inp.unget()
            inp.fail("Expected open paren, symbol, or epsilon")
            pass
        return SymRegex(c)

    def rtail(lhs):
        if inp.peek() == '|':
            inp.get()
            x = parseC()
            return rtail(OrRegex(lhs, x))
        return lhs

    def ctail(lhs):
        if inp.peek() is not None and inp.peek() not in '|*)':
            temp = parseS()
            return ctail(ConcatRegex(lhs, temp))
        return lhs

    def stars(lhs):
        while inp.peek() == '*':
            inp.eat('*')
            lhs = StarRegex(lhs)
            pass
        return lhs

    return parseR()
