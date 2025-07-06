from turing_machine import TuringMachine

if __name__ == '__main__':
    input_str = input("Enter a string of a's and b's: ").strip()
    tm = TuringMachine(input_str)
    result = tm.run()
    print("Result:", result)
