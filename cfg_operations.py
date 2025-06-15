class CFG:
    def __init__(self):
        self.variables = set()
        self.terminals = set()
        self.productions = {} # str -> list(str)
        self.start = ''

    def __str__(self):
        s = "# Variables\n"
        s += " ".join(map(str, self.variables))
        s += "\n# Terminals\n"
        s += " ".join(map(str, self.terminals))
        s += "\n# Start Symbol\n"
        s += self.start
        s += "\n# Productions\n"
        
        for (lhs, rhs) in self.productions.items():
            for r in rhs:
                s += f"{lhs} -> {r}\n"

        return s
    
    def add_production(self, lhs, rhs):
        if lhs not in self.variables:
            print(f"Production {lhs} -> {rhs} does not follow context-free grammar rules.")
            return
        self.productions.setdefault(lhs, []).append(rhs)

def get_nullables(cfg):
    old_nullables = set()
    new_nullables = set()
    for lhs, rhs in cfg.productions.items():
        for r in rhs:
            if r == "Ɛ":
                print(f"rhs is epsilon: {lhs} -> {r}")
                new_nullables.add(lhs)

    while old_nullables != new_nullables:
        old_nullables = new_nullables
        for lhs, rhs in cfg.productions.items():
            for r in rhs:
                flag = False
                for c in r:   # parse string
                    if c not in old_nullables:
                        flag = True
                    if flag == False:
                        new_nullables.add(lhs)
        
    return old_nullables


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

    print(get_nullables(cfg))
