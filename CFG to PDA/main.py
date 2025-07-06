from parser import parse_cfg_from_input, process_cfg_to_pda
from cfg_operations import convert_to_gnf

def main():
    cfg = parse_cfg_from_input()
    pda = process_cfg_to_pda(cfg)
    print("\nGenerated PDA:\n")
    print(pda)


if __name__ == "__main__":
    main()
