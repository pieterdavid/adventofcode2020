# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.7.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# # Advent of code 2020: day 19
#
# Problem [here](https://adventofcode.com/2020/day/19)

# ## Part 1

# +
class StrRule:
    def __init__(self, sub):
        self.sub = sub
    def __call__(self, pattern, start=0):
        yield from ([ start+len(self.sub) ] if pattern[start:start+len(self.sub)] == self.sub else [])
    def __str__(self):
        return self.sub

class SeqRule:
    def __init__(self, parts):
        self.parts = parts
    def __call__(self, pattern, start=0, parts=None):
        if parts is None:
            parts = self.parts
        if len(parts) > 1:
            for m in parts[0](pattern, start=start):
                yield from self(pattern, start=m, parts=parts[1:])
        else:
            yield from parts[0](pattern, start=start)
    def __str__(self):
        return " ".join(str(p) for p in self.parts)

class OrRule:
    def __init__(self, options):
        self.options = options
    def __call__(self, pattern, start=0):
        for opt in self.options:
            yield from opt(pattern, start=start)
    def __str__(self):
        return "( {0} )".format(" | ".join(str(p) for p in self.options))
    
def parseRule(rule, allRulesIn, allRules):
    if rule.startswith('"') and rule.endswith('"'):
        pRule = StrRule(rule[1:-1])
    elif "|" in rule:
        pRule = OrRule([ parseRule(tok, allRulesIn, allRules) for tok in rule.split(" | ") ])
    elif all(tk.isnumeric() for tk in rule.split()):
        ids = [ int(tk) for tk in rule.split() ]
        for iTk in ids:
            if iTk not in allRules:
                allRules[iTk] = parseRule(allRulesIn[iTk], allRulesIn, allRules)
        pRule = SeqRule([ allRules[iP] for iP in ids ])
    else:
        raise RuntimeError(f"Invalid rule: {rule}")
    return pRule

ex1_in = dict((int(ln.split(": ")[0]), ln.split(": ")[1]) for ln in '''0: 1 2
1: "a"
2: 1 3 | 3 1
3: "b"'''.split("\n"))

ex1_p = dict()
ex1_r0 = parseRule(ex1_in[0], ex1_in, ex1_p)
print(ex1_r0)

# +
ex2_in = dict((int(ln.split(": ")[0]), ln.split(": ")[1]) for ln in '''0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"'''.split("\n"))

ex2_p = dict()
ex2_r0 = parseRule(ex2_in[0], ex2_in, ex2_p)
print(ex2_r0)

ex2_msg = list("""ababbb
bababa
abbbab
aaabbb
aaaabbb""".split("\n"))
for msg in ex2_msg:
    if any(end == len(msg) for end in ex2_r0(msg)):
        print(f"'{msg}' passes the rule")
    else:
        print(f"'{msg}' does not pass the rule")
# -

p_rules = {}
p_msg = []
with open("inputs/day19.txt") as inF:
    lines = iter(inF)
    try:
        ln = next(lines).strip()
        while ln:
            num, rule = ln.split(": ")
            p_rules[int(num)] = rule
            ln = next(lines).strip()
        ln = next(lines).strip()
        while ln:
            p_msg.append(ln)
            ln = next(lines).strip()
    except StopIteration:
        pass

p_p = dict() # parsed rules memo
p_r0 = parseRule(p_rules[0], p_rules, p_p)
nMatch = 0
for msg in p_msg:
    if any(end == len(msg) for end in p_r0(msg)):
        nMatch += 1
print(f"{nMatch:d} out of {len(p_msg):d} messages match")


# ## Part 2
#
# Changed the classes above to yield all matches instead of returning the first match only, and changed matching criteria to any.

# +
class DelegatingRule: # inserted to avoid infinite recursion with eager parsing
    def __init__(self, allRules, idx):
        self.allRules = allRules
        self.idx = idx
    def __call__(self, pattern, start=0):
        yield from self.allRules[self.idx](pattern, start=start)
    def __str__(self):
        return f"#{self.idx}"

def parseRule_v2(rule, allRulesIn, allRules, stack=None):
    if rule.startswith('"') and rule.endswith('"'):
        pRule = StrRule(rule[1:-1])
    elif "|" in rule:
        pRule = OrRule([ parseRule_v2(tok, allRulesIn, allRules, stack=stack) for tok in rule.split(" | ") ])
    elif all(tk.isnumeric() for tk in rule.split()):
        ids = [ int(tk) for tk in rule.split() ]
        itemRules = []
        for iTk in ids:
            if iTk in stack:
                itemRules.append(DelegatingRule(allRules, iTk))
            else:
                if iTk not in allRules:
                    allRules[iTk] = parseRule_v2(allRulesIn[iTk], allRulesIn, allRules, stack=stack+[iTk])
                itemRules.append(allRules[iTk])
        pRule = SeqRule(itemRules)
    else:
        raise RuntimeError(f"Invalid rule: {rule}")
    return pRule


# +
ex3_rules = dict((int(ln.split(": ")[0]), ln.split(": ")[1]) for ln in '''42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1'''.split("\n"))
ex3_msg = list('''abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba'''.split("\n"))

p_ex3 = dict()
ex3_r0 = parseRule_v2(ex3_rules[0], ex3_rules, p_ex3, stack=[0])

for msg in ex3_msg:
    if any(end == len(msg) for end in ex3_r0(msg)):
        print(f"'{msg}' passes the rule")
# -

ex3_rules_m = dict(ex3_rules)
ex3_rules_m[8] = "42 | 42 8"
ex3_rules_m[11] = "42 31 | 42 11 31"
p_ex3_m = dict()
ex3_m_r0 = parseRule_v2(ex3_rules_m[0], ex3_rules_m, p_ex3_m, stack=[0])
for msg in ex3_msg:
    if any(end == len(msg) for end in ex3_m_r0(msg)):
        print(f"'{msg}' passes the rule")

# +
p_rules_2 = dict(p_rules)
p_rules_2[8] = "42 | 42 8"
p_rules_2[11] = "42 31 | 42 11 31"

p_p2 = dict() # parsed rules memo
p2_r0 = parseRule_v2(p_rules_2[0], p_rules_2, p_p2, stack=[0])
nMatch2 = 0
for msg in p_msg:
    if any(end == len(msg) for end in p2_r0(msg)):
        nMatch2 += 1
print(f"{nMatch2:d} out of {len(p_msg):d} messages match")
# -
