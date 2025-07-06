from cfg_operations import convert_to_gnf

class PDA:
    def __init__(self):
        self.states = set()
        self.input_alphabet = set()
        self.stack_alphabet = set()
        self.transitions = {}
        self.initial_state = None
        self.stack_start_symbol = None
        self.final_states = set()

    def __str__(self):
        s = "PDA:\n"
        s += f"States: {self.states}\n"
        s += f"Input Symbols: {self.input_alphabet}\n"   
        s += f"Stack Symbols: {self.stack_alphabet}\n"
        s += f"Transitions:\n"
        for (state, input_symbol, pop_symbol), (next_state, push_symbol) in self.transitions.items():
            s += f"  ({state}, {input_symbol}, {pop_symbol}) -> ({next_state}, {push_symbol})\n"
        s += f"Initial State: {self.initial_state}\n"
        s += f"Initial Stack Symbol: {self.stack_start_symbol}\n" 
        s += f"Final States: {self.final_states}\n"
        return s
    
    def add_transition(self, state, input_symbol, pop_symbol, next_state, push_symbol):
        self.transitions[(state, input_symbol, pop_symbol)] = (next_state, push_symbol)

    def remove_transition(self, state, input_symbol, pop_symbol, next_state, push_symbol):
        if ((state, input_symbol, pop_symbol), (next_state, push_symbol)) in self.transitions.items():
            self.transitions.pop((state, input_symbol, pop_symbol))
    

def cfg_to_pda(cfg):
    cfg = convert_to_gnf(cfg)

    pda = PDA()
    pda.states = {'q_start', 'q_loop', 'q_accept'}
    pda.input_alphabet = cfg.terminals
    pda.stack_alphabet = cfg.variables.union(cfg.terminals).union({'$'})
    pda.initial_state = 'q_start'
    pda.stack_start_symbol = '$'
    pda.final_states = {'q_accept'}

    pda.add_transition('q_start', 'Ɛ', 'Ɛ', 'q_loop', cfg.start + '$')

    print(cfg.productions.items())

    for (var, rhss) in cfg.productions.items():
        for rhs in rhss:
            a = rhs[0]  
            symbols_to_push = rhs[1:] 
            if symbols_to_push:
                push = ''.join(reversed(symbols_to_push)) 
            else:
                push = 'Ɛ'
            pda.add_transition('q_loop', a, var, 'q_loop', push)

    pda.add_transition('q_loop', 'Ɛ', '$', 'q_accept', 'Ɛ')

    return pda

if __name__ == "__main__":
    pass
