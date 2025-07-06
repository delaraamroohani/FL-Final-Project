from parser import parse_cfg_from_input, process_cfg_to_pda

def main():
    cfg = parse_cfg_from_input()
    pda = process_cfg_to_pda(cfg)
    print("\nGenerated PDA:\n")
    print(pda)


if __name__ == "__main__":
    main()
