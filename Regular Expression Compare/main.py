import copy
from regex import *
from state import *
from nfa import *
from dfa import *


# You should write this function.
# It takes an NFA and returns a DFA.
def nfaToDFA(nfa):
    dfa = DFA()
    dfa_map, nfa_map = dict(), dict()

    nfa_state_num = len(nfa.states)

    dfa.alphabet = copy.deepcopy(nfa.alphabet)
    if '&' in dfa.alphabet:
        dfa.alphabet.remove('&')
    dfa.states = [State(0)]
    start_state = set(nfa.epsilonClose(nfa.states[0]))
    start_state.add(nfa.states[0])
    dfa_map[0] = start_state
    dfa.is_accepting[0] = False

    # eliminate all epsilon transition
    for i in range(nfa_state_num):
        for sym, ss in nfa.states[i].transition.items():
            cur_ss = set()
            for s in ss:
                cur_ss.add(s)
                cur_ss.update(nfa.epsilonClose(s))
            nfa_map[(i, sym)] = cur_ss

    # construct DFA
    visited = set()
    queue = [dfa.states[0]]
    while queue:
        curr_state = queue.pop(0)
        if curr_state in visited:
            continue
        state_include = dfa_map[curr_state.id]
        for sym in dfa.alphabet:
            next_states = set()
            for s in state_include:
                if (s.id, sym) in nfa_map:
                    next_states.update(nfa_map[(s.id, sym)])
            if next_states in dfa_map.values():
                for k, v in dfa_map.items():
                    if next_states == v:
                        dfa.addTransition(dfa.states[curr_state.id], dfa.states[k], sym)
                        queue.append(dfa.states[k])
                        break
            else:
                curr_len = len(dfa.states)
                dfa_map[curr_len] = next_states
                dfa.states.append(State(curr_len))
                dfa.is_accepting[curr_len] = False
                dfa.addTransition(dfa.states[curr_state.id], dfa.states[curr_len], sym)
                queue.append(dfa.states[curr_len])
        visited.add(curr_state)

    # set accepting states
    for i, nfa_states in dfa_map.items():
        for s in nfa_states:
            if nfa.is_accepting[s.id]:
                dfa.is_accepting[i] = True
                break

    return dfa


# You should write this function.
# It takes an DFA and returns a NFA.
def dfaToNFA(dfa):
    nfa = NFA()
    nfa.states = copy.deepcopy(dfa.states)
    nfa.is_accepting = copy.deepcopy(dfa.is_accepting)
    nfa.alphabet = copy.deepcopy(dfa.alphabet)
    return nfa


# You should write this function.
# It takes two regular expressions and returns a 
# boolean indicating if they are equivalent
def equivalent(re1, re2):
    nfa1 = re1.transformToNFA()
    nfa2 = re2.transformToNFA()
    dfa1 = nfaToDFA(nfa1)
    dfa2 = nfaToDFA(nfa2)
    dfa1.complement()
    dfa2.complement()
    nfa_1c = dfaToNFA(dfa1)
    nfa_2c = dfaToNFA(dfa2)
    nfa_1m = nfaUnion(nfa_1c, nfa2)
    nfa_2m = nfaUnion(nfa1, nfa_2c)
    dfa_1m = nfaToDFA(nfa_1m)
    dfa_2m = nfaToDFA(nfa_2m)
    dfa_1m.complement()
    dfa_2m.complement()

    for i in dfa_1m.is_accepting:
        if dfa_1m.is_accepting[i]:
            return False
    for i in dfa_2m.is_accepting:
        if dfa_2m.is_accepting[i]:
            return False
    return True


if __name__ == "__main__":
    def testNFA(strRe, s, expected):
        re = parse_re(strRe)
        # test your nfa conversion
        nfa = re.transformToNFA()
        res = nfa.isStringInLanguage(s)
        if res == expected:
            print(strRe, " gave ", res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res, " on ", s, " but expected ", expected)
            pass
        pass


    def testDFA(strRe, s, expected):
        # test your dfa conversion
        re = parse_re(strRe)
        nfa = re.transformToNFA()
        dfa = nfaToDFA(nfa)
        res = dfa.isStringInLanguage(s)
        if res == expected:
            print(strRe, " gave ", res, " as expected on ", s)
        else:
            print("**** ", strRe, " Gave ", res, " on ", s, " but expected ", expected)
            pass
        pass


    def testEquivalence(strRe1, strRe2, expected):
        re1 = parse_re(strRe1)
        re2 = parse_re(strRe2)

        res = equivalent(re1, re2)
        if res == expected:
            print("Equivalence(", strRe1, ", ", strRe2, ") = ", res, " as expected.")
        else:
            print("Equivalence(", strRe1, ", ", strRe2, ") = ", res, " but expected ", expected)
            pass
        pass


    def pp(r):
        print()
        print("Starting on " + str(r))
        re = parse_re(r)
        print(repr(re))
        print(str(re))
        pass


    # test your NFA
    testNFA('a*', '', True)
    testNFA('a*', 'a', True)
    testNFA('a*', 'aaa', True)
    testNFA('a|b', '', False)
    testNFA('a|b', 'a', True)
    testNFA('a|b', 'b', True)
    testNFA('a|b', 'ab', False)
    testNFA('ab|cd', '', False)
    testNFA('ab|cd', 'ab', True)
    testNFA('ab|cd', 'cd', True)
    testNFA('ab|cd*', '', False)
    testNFA('ab|cd*', 'c', True)
    testNFA('ab|cd*', 'cd', True)
    testNFA('ab|cd*', 'cddddddd', True)
    testNFA('ab|cd*', 'ab', True)
    testNFA('((ab)|(cd))*', '', True)
    testNFA('((ab)|(cd))*', 'ab', True)
    testNFA('((ab)|(cd))*', 'cd', True)
    testNFA('((ab)|(cd))*', 'abab', True)
    testNFA('((ab)|(cd))*', 'abcd', True)
    testNFA('((ab)|(cd))*', 'cdcdabcd', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', '', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'ab', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'abcd', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'cd', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'dfgab', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'defg', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'deeefg', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hkln', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'q', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijkln', True)
    testNFA('((ab|cd)*|(de*fg|h(ij)*klm*n|q))*', 'hijijklmmmmmmmmmmn', True)

