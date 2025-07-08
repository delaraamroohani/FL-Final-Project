# parser.py
from cfg_operations import CFG, convert_to_gnf
from pda_operations import PDA, cfg_to_pda

def parse_cfg_from_input():
    print("Enter your grammar line by line. End input with an empty line.")
    print("Format each production as: A -> aB or A -> Ɛ")

    cfg = CFG()
    lines = []

    while True:
        line = input()
        if line.strip() == "":
            break
        lines.append(line)

    for line in lines:
        if '->' not in line:
            continue
        lhs, rhs = map(str.strip, line.split("->"))
        if not cfg.start:
            cfg.start = lhs
        cfg.variables.add(lhs)
        for symbol in rhs:
            if symbol.isupper() and symbol != 'Ɛ':
                cfg.variables.add(symbol)
            elif symbol.islower() and symbol != 'Ɛ':
                cfg.terminals.add(symbol)
        cfg.add_production(lhs, rhs)

    return cfg

def process_cfg_to_pda(cfg):
    # print("\nOriginal CFG:\n")
    # print(cfg)
    # gnf_cfg = convert_to_gnf(cfg)
    # print("\nCFG in Greibach Normal Form (GNF):\n")
    # print(gnf_cfg)
    pda = cfg_to_pda(cfg)
    return pda
