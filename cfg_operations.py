import copy

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
            print(f"Production {lhs} -> {rhs} does not follow context-free grammar rules.")
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
                print(f"rhs is epsilon: {lhs} -> {rhs}")
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
                            new_prod.setdefault(lhs, set()).add(split[0] + split[1])
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

    print(remove_null_productions(cfg))
