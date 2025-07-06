class TuringMachine:
    def __init__(self, tape_str):
        self.tape = ['_'] * 10 + list(tape_str) + ['_'] * 10
        self.head = 10
        self.state = 'q0'
        self.accepted = False

    def read(self):
        return self.tape[self.head]
    
    def write(self, symbol):
        self.tape[self.head] = symbol

    def move(self, direction):
        if direction == 'R':
            self.head += 1
        elif direction == 'L':
            self.head -= 1

    def step(self):
        if self.state == 'q0':
            if self.read() == 'a':
                self.write('_')
                self.move('R')
                self.state = 'q1'

            elif self.read() == 'b':
                self.write('_')
                self.move('R')
                self.state = 'q4'

            elif self.read() == '_':
                self.write('_')
                self.move('L')
                self.state = 'Y'

        elif self.state == 'q1':
            if self.read() == 'a':
                self.write('a')
                self.move('R')
                self.state = 'q2'

            elif self.read() == 'b':
                self.write('b')
                self.move('R')
                self.state = 'q2'

            elif self.read() == '_':
                self.write('_')
                self.move('L')
                self.state = 'Y'

        elif self.state == 'q2':
            if self.read() == 'a':
                self.write('a')
                self.move('R')
                self.state = 'q2'

            elif self.read() == 'b':
                self.write('b')
                self.move('R')
                self.state = 'q2'

            elif self.read() == '_':
                self.write('_')
                self.move('L')
                self.state = 'q3'
        
        elif self.state == 'q3':
            if self.read() == 'a':
                self.write('_')
                self.move('L')
                self.state = 'q7'

            elif self.read() == 'b':
                self.write('_')
                self.move('L')
                self.state = 'q9'

        elif self.state == 'q4':
            if self.read() == 'a':
                self.write('a')
                self.move('R')
                self.state = 'q5'

            elif self.read() == 'b':
                self.write('b')
                self.move('R')
                self.state = 'q5'

            elif self.read() == '_':
                self.write('_')
                self.move('L')
                self.state = 'Y'

        elif self.state == 'q5':
            if self.read() == 'a':
                self.write('a')
                self.move('R')
                self.state = 'q5'

            elif self.read() == 'b':
                self.write('b')
                self.move('R')
                self.state = 'q5'

            elif self.read() == '_':
                self.write('_')
                self.move('L')
                self.state = 'q6'

        elif self.state == 'q6':
            if self.read() == 'b':
                self.write('_')
                self.move('L')
                self.state = 'q7'

            elif self.read() == 'a':
                self.write('_')
                self.move('L')
                self.state = 'q9'

        elif self.state == 'q7':
            if self.read() == 'a':
                self.write('a')
                self.move('L')
                self.state = 'q7'

            elif self.read() == 'b':
                self.write('b')
                self.move('L')
                self.state = 'q7'

            elif self.read() == '_':
                self.write('_')
                self.move('R')
                self.state = 'q0'

        elif self.state == 'Y':
            if self.read() == '_':
                self.write('Y')
                self.move('R')
                self.state = 'E'

        elif self.state == 'E':
            if self.read() == '_':
                self.write('E')
                self.move('R')
                self.state = 'S'

        elif self.state == 'S':
            if self.read() == '_':
                self.write('S')
                self.move('R')
                self.state = 'accepted'

        elif self.state == 'q9':
            if self.read() == 'a':
                self.write('_')
                self.move('L')
                self.state = 'q9'

            elif self.read() == 'b':
                self.write('_')
                self.move('L')
                self.state = 'q9'

            elif self.read() == '_':
                self.write('_')
                self.move('R')
                self.state = 'N'

        elif self.state == 'N':
            if self.read() == '_':
                self.write('N')
                self.move('R')
                self.state = 'O'

        elif self.state == 'O':
            if self.read() == '_':
                self.write('O')
                self.move('R')
                self.state = 'accepted'

        elif self.state == 'accepted':
            self.accepted = True

    def run(self):
        while not self.accepted:
            self.step()
        return ''.join(self.tape).strip('_')