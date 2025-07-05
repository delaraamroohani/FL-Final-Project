import copy
from collections import deque

alphabet_lower = list("abcdefghijklmnopqrstuvwxyz")
alphabet_upper = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
alphabet_lower_pointer = 0
alphabet_upper_pointer = 0

class CFG:
    def __init__(self):
        self.variables = set()
        self.terminals = set()
        self.productions = {} # str -> set(str)
        self.start = ''

    def __str__(self):
        s = "# Variables\n"
        s += " ".join(map(str, self.variables))
        s += "\n# Terminals\n"
        s += " ".join(map(str, self.terminals))
        s += "\n# Start Symbol\n"
        s += self.start
        s += "\n# Productions\n"
        
        for (lhs, rhss) in self.productions.items():
            for rhs in rhss:
                s += f"{lhs} -> {rhs}\n"

        return s
    
    def add_production(self, lhs, rhs):
        if lhs not in self.variables:
            print(f"Production {lhs} -> {rhs} does not follow context-free "
                  "grammar rules.")
            return
        self.productions.setdefault(lhs, set()).add(rhs)

    def remove_production(self, lhs, rhs):
        self.productions.get(lhs).remove(rhs)


def get_nullables(cfg):
    old_nullables = set()
    new_nullables = set()
    for lhs, rhss in cfg.productions.items():
        for rhs in rhss:
            if rhs == "Ɛ":
                new_nullables.add(lhs)

    while old_nullables != new_nullables:
        old_nullables = new_nullables
        for lhs, rhss in cfg.productions.items():
            for rhs in rhss:
                flag = False
                for c in rhs:   # parse string
                    if c not in old_nullables:
                        flag = True
                    if flag == False:
                        new_nullables.add(lhs)
        
    return old_nullables


def remove_null_productions(old_cfg):
    cfg = copy.deepcopy(old_cfg)
    nullables = get_nullables(cfg)

    for lhs, rhss in cfg.productions.items():
        rhss_frozen = frozenset(rhss)
        for rhs in rhss_frozen:
            if rhs == "Ɛ":
                cfg.remove_production(lhs, rhs)

    old_prod = {}
    new_prod = copy.deepcopy(cfg.productions)

    while old_prod != new_prod:
        old_prod = copy.deepcopy(new_prod)
        new_prod = {}
        for lhs, rhss in old_prod.items():
            for rhs in rhss:
                if len(rhs) > 1:
                    for c in rhs:
                        if c in nullables:
                            split = rhs.split(c, 1)
                            cfg.add_production(lhs, split[0] + split[1])
                            (new_prod.setdefault(lhs, set())
                             .add(split[0] + split[1]))
    return cfg


def get_unit_production_graph(cfg):
    graph = {}
    for lhs, rhss in cfg.productions.items():
        for rhs in rhss:
            if rhs in cfg.variables:
                graph.setdefault(lhs, set()).add(rhs)
    cur = graph
    new = {}
    flag = False

    while not flag:
        for lhs, rhss in cur.items():
            for rhs in rhss:
                if rhs in graph.keys():
                    for rhs2 in graph.get(rhs):
                        if (rhs2 != lhs 
                            and (lhs not in graph.keys() 
                                 or rhs2 not in graph.get(lhs))):
                            new.setdefault(lhs, set()).add(rhs2)
        
        for lhs, rhs in graph.items():
            if lhs in new.keys():
                rhs.update(new.get(lhs))

        cur = new
        if len(new.items()) == 0:
            flag = True
        new = {}

    return graph


def remove_unit_productions(old_cfg):
    unit_prod = get_unit_production_graph(old_cfg)
    cfg = copy.deepcopy(old_cfg)

    for lhs, rhss in cfg.productions.items():
        rhss_frozen = frozenset(rhss)
        for rhs in rhss_frozen:
            if rhs in cfg.variables:
                cfg.productions.get(lhs).remove(rhs)

    for lhs, rhss in unit_prod.items():
        for rhs in rhss:
            (cfg.productions.setdefault(lhs, set())
             .update(cfg.productions.get(rhs)))

    return cfg


def get_non_generating_symbols(cfg):
    old = set()
    new = set()

    for lhs, rhss in cfg.productions.items():
        for rhs in rhss:
            flag = False
            for c in rhs:
                if c not in cfg.terminals and c != "Ɛ":
                    flag = True
            if flag == False:
                new.add(lhs)

    while old != new:
        old = copy.deepcopy(new)
        for lhs, rhss in cfg.productions.items():
            for rhs in rhss:
                flag = False
                for c in rhs:
                    if c not in cfg.terminals and c not in old:
                        flag = True
                if flag == False:
                    new.add(lhs)
            
    non_gen = cfg.variables.difference(old)
    return non_gen


def get_unreachable_symbols(cfg):
    old = set()
    new = set()

    new.add(cfg.start)

    while old != new:
        old = copy.deepcopy(new)
        for lhs, rhss in cfg.productions.items():
            if lhs in old:
                for rhs in rhss:
                    for c in rhs:
                        if c in cfg.variables:
                            new.add(c)
    
    unreachable = cfg.variables.difference(old)
    return unreachable


def remove_useless_productions(old_cfg):
    cfg = copy.deepcopy(old_cfg)
    non_gen = get_non_generating_symbols(cfg)

    for lhs, rhss in cfg.productions.items():
        if lhs in non_gen:
            cfg.productions.get(lhs).clear()
        else:
            rhss_frozen = frozenset(rhss)
            for rhs in rhss_frozen:
                for c in rhs:
                    if c in non_gen:
                        rhss.remove(rhs)

    unreachable = get_unreachable_symbols(cfg)

    for lhs, rhss in cfg.productions.items():
        if lhs in unreachable:
            cfg.productions.get(lhs).clear()
        else:
            for rhs in rhss:
                for c in rhs:
                    if c in unreachable:
                        rhss.remove(rhs)

    return cfg


def convert_to_gcnf(old_cfg): # a GCNF is a Generalised Chomsky Normal Form
    cfg = copy.deepcopy(old_cfg)
    cfg = remove_null_productions(cfg)
    cfg = remove_unit_productions(cfg)
    cfg = remove_useless_productions(cfg)

    terminal_productions = set()
    for lhs, rhss in cfg.productions.items():
        for rhs in rhss:
            if len(rhs) == 1 and rhs[0] in cfg.terminals:
                terminal_productions.add((lhs, rhs))

    for lhs, rhss in cfg.productions.items():
        rhss_frozen = frozenset(rhss)
        for rhs in rhss_frozen:
            if len(rhs) > 1:
                cfg.remove_production(lhs, rhs)
                for r in rhs:
                    if r in cfg.terminals:
                        flag = False
                        for v, t in terminal_productions:
                            if t == r:
                                flag = True
                                rhs = rhs.replace(r, v)
                        if not flag:
                            global alphabet_upper, alphabet_upper_pointer
                            terminal_productions.add((alphabet_upper[alphabet_upper_pointer], r))
                            rhs = rhs.replace(r, alphabet_upper[alphabet_upper_pointer])
                            alphabet_upper_pointer += 1
                cfg.add_production(lhs, rhs)

    return cfg


def remove_left_recursion(var, prod):
    prods = {}

    global alphabet_upper, alphabet_upper_pointer
    recursive_parts = set()
    nonrecursive_parts = set()
    z = alphabet_upper[alphabet_upper_pointer]
    alphabet_upper_pointer += 1
    for rhs in prod:
        if rhs[0] == var:
            recursive_parts.add(rhs[1:])
        else:
            nonrecursive_parts.add(rhs)

    if not recursive_parts:
        return {var: nonrecursive_parts}

    for y in nonrecursive_parts:
        prods.setdefault(var, set()).add(y)
        prods.setdefault(var, set()).add(y + z)
    for x in recursive_parts:
        prods.setdefault(z, set()).add(x)
        prods.setdefault(z, set()).add(x + z)

    return prods


def convert_to_gnf(old_cfg):
    cfg = convert_to_gcnf(old_cfg)
    
    ordered_variables = list(cfg.variables)
    new_productions = {var: set() for var in ordered_variables}

    changed = True

    while changed:
        changed = False
        recursive = False
        for cur in ordered_variables:
            i = ordered_variables.index(cur)
            updated = set()

            for rhs in cfg.productions[cur]:
                if rhs[0] in cfg.variables:
                    j = ordered_variables.index(rhs[0])
                    if j < i:
                        for r in cfg.productions[rhs[0]]:
                            updated.add(r + rhs[1:])
                    elif j == i:
                        recursive = True
                    else:
                        updated.add(rhs)
                else:
                    updated.add(rhs)

            if updated != cfg.productions[cur]:
                changed = True
                cfg.productions[cur] = updated

            if recursive:
                remove_left_recursion(cur, cfg.productions[cur])

    for cur in ordered_variables:
        gnf_rhs = set()
        for rhs in cfg.productions[cur]:
            if rhs[0] in cfg.variables:
                queue = deque(rhs)
                while queue:
                    current = queue.popleft()
                    if current[0] in cfg.variables:
                        for p in cfg.productions[current[0]]:
                            queue.append(p + current[1:])
                    else:
                        gnf_rhs.add(current)
            else:
                gnf_rhs.add(rhs)
        new_productions[cur] = gnf_rhs

    cfg.productions = new_productions
    return cfg

if __name__ == "__main__":
    cfg = CFG()
    cfg.start = 'S'
    cfg.terminals = {'a', 'b', 'd'}
    cfg.variables = {'S', 'A', 'B', 'C', 'D'}
    cfg.add_production('S', "ABaC")
    cfg.add_production('A', "BC")
    cfg.add_production('B', "b")
    cfg.add_production('B', "Ɛ")
    cfg.add_production('C', "D")
    cfg.add_production('C', "Ɛ")
    cfg.add_production('D', "d")

    # cfg.start = 'S'
    # cfg.variables = {'S', 'A', 'B', 'C', 'D'}
    # cfg.terminals = {'a', 'c', 'd'}
    # cfg.add_production("S", "a")
    # cfg.add_production("S", "aA")
    # cfg.add_production("S", "B")
    # cfg.add_production("S", "C")
    # cfg.add_production("A", "aB")
    # cfg.add_production("A", "Ɛ")
    # cfg.add_production("B", "Aa")
    # cfg.add_production("C", "cCD")
    # cfg.add_production("D", "ddd")

    print(convert_to_gnf(cfg))
