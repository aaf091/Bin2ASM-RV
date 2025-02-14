from mongo_handler import MongoHandler
from decoding import *
from formatting import *

# Initialize MongoDB handler
db = MongoHandler()

def process_instruction(binary_code, format_option):
    """Process a given binary instruction by checking the database first."""
    # Check if translation exists in MongoDB
    cached_translation = db.get_translation(binary_code)
    if cached_translation:
        print(f"Retrieved from DB: {cached_translation}")
        return cached_translation

    # Decode the instruction using `inst_decode`
    assembly_code = inst_decode(binary_code, options=format_option)

    # Store result in MongoDB
    db.store_translation(binary_code, assembly_code)

    print(f"Decoded: {assembly_code}")
    return assembly_code

def show_translation_history():
    """Display translation history from MongoDB with reformatting options."""
    history = db.get_translation_history(limit=10)
    
    if not history:
        print("No translation history found.")
        return

    print("\n=== Translation History ===")
    
    # Allow user to reformat output
    print("Choose formatting option for constants:")
    print("[Enter] Decimal (Default)")
    print("[sb] Binary")
    print("[sx] Hexadecimal")
    format_option = input("Formatting option: ").strip() or "Enter"

    if format_option.lower() not in ["sb", "sx"]:
        format_option = "Enter"

    # Print formatted history
    for record in history:
        binary_code = record["binary_code"]
        assembly_code = inst_decode(binary_code, options=format_option)  # Reformat with user choice
        print(f"{binary_code}  →  {assembly_code} (Time: {record['timestamp']})")

    print("===========================\n")

def inst_type(instruction):
    """Determine the instruction format based on the opcode."""
    format_type = ''
    opcode = instruction[25:len(instruction) + 1]

    if opcode == '1101111': format_type = 'UJ'
    elif opcode == '1100011': format_type = 'SB'
    elif opcode == '0100011': format_type = 'S'
    elif opcode == '0110111' or opcode == '0010111': format_type = 'U'
    elif opcode == '0000011' or opcode == '1100111' or opcode == '0010011': format_type = 'I'
    elif opcode == '0110011': format_type = 'R'

    return format_type

def inst_decode(instruction, options):
    """Decode the instruction based on its type."""
    format_type = inst_type(instruction)

    match format_type:
        case 'R':
            contents = {}
            contents['funct7'], contents['rs2'], contents['rs1'], contents['funct3'], contents['rd'], contents['opcode'] = decode_R(instruction)
            return format_R(contents, options)
        case 'SB':
            contents = {}
            contents['imm_cycle_32'], contents['rs2'], contents['rs1'], contents['funct3'], contents['imm_offset'], contents['opcode'] = decode_SB(instruction)
            return format_SB(contents, options)
        case 'S':
            contents = {}
            contents['imm_cycle_32'], contents['rs2'], contents['rs1'], contents['funct3'], contents['imm_offset'], contents['opcode'] = decode_S(instruction)
            return format_S(contents, options)
        case 'I':
            imm, rs1, funct3, rd, opcode = decode_I(instruction)
            contents = {}

            # If it's logical shift, format differently
            if ((opcode == '0010011' and (funct3 != '001' and funct3 != '101')) or opcode == '0000011'):
                contents['imm'] = imm
                contents['rs1'] = rs1
                contents['funct3'] = funct3
                contents['rd'] = rd
                contents['opcode'] = opcode
            else:
                funct7, shamt, rs1, funct3, rd, opcode = decode_R(instruction)
                contents['funct7'] = funct7
                contents['shamt'] = shamt
                contents['rs1'] = rs1
                contents['funct3'] = funct3
                contents['rd'] = rd
                contents['opcode'] = opcode

            return format_I(contents, options)
        case 'U':
            return 'U and UJ functions not implemented'
        case 'UJ':
            return 'U and UJ functions not implemented'

def main():
    """CLI Menu for the Translator"""
    while True:
        print("\nOptions:")
        print("1. Translate a RISC-V instruction")
        print("2. View translation history (with reformatting)")
        print("3. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            binary_code = input("Enter binary or hex instruction: ").strip()
            
            # Ask for formatting preference
            print("Choose formatting option for constants:")
            print("[Enter] Decimal (Default)")
            print("[sb] Binary")
            print("[sx] Hexadecimal")
            format_option = input("Formatting option: ").strip() or "Enter"

            # Normalize default case
            if format_option.lower() not in ["sb", "sx"]:
                format_option = "Enter"

            process_instruction(binary_code, format_option)

        elif choice == "2":
            show_translation_history()

        elif choice == "3":
            print("Exiting...")
            break

        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    main()