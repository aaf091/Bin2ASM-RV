import yaml

def _rname(reg_add):
    xname = f'x{int(reg_add, 2)}'
    stream = open('regs.yaml', 'r')
    regs = yaml.load(stream, Loader=yaml.FullLoader)

    return regs[xname]


def _calc_imm(contents):
    cycle = int(contents['imm_cycle_32'], 2)
    imm = int(contents['imm_offset'], 2)

    return imm + (cycle * 32)


def _conv_bx(value, options):
    base = 10
    match options:
        case ('sb'): base = 2
        case ('sx'): base = 16

    match base:
        case (2): return bin(value)
        case (16): return hex(value)
    
    return value


# Dont use options yet
def format_R(contents, options):
    inst = ''
    stream = open('instructions.yaml', 'r')
    instrucoes = yaml.load(stream, Loader=yaml.FullLoader)

    for dict in instrucoes['R']:
        if contents['funct7'] == dict['funct7'] and contents['funct3'] == dict['funct3']:
            inst = dict['name']

    return f"{inst} {_rname(contents['rd'])}, {_rname(contents['rs1'])}, {_rname(contents['rs2'])}"


def format_I(contents, options):
    inst = ''
    stream = open('instructions.yaml', 'r')
    instrucoes = yaml.load(stream, Loader=yaml.FullLoader)

    for dict in instrucoes['I']:
        if contents['funct3'] == dict['funct3'] and contents['opcode'] == dict['opcode']: inst = dict['name']

    # Formatting for immediate logic instructions
    if (len(contents) == 5):
        if contents['opcode'] == '0010011':
            return f"{inst} {_rname(contents['rd'])}, {_rname(contents['rs1'])}, {_conv_bx(int(contents['imm'], 2), options)}"
        # Formatting for load instructions
        elif contents['opcode'] == '0000011':
            return f"{inst} {_rname(contents['rd'])}, {contents['imm']}({_rname(contents['rs1'])})"
    # Formatting for shift statements
    else:
        return f"{inst} {_rname(contents['rd'])}, {_rname(contents['rs1'])}, {_conv_bx(int(contents['shamt'], 2), options)}"


def format_SB(contents, options):
    inst = ''
    stream = open('instructions.yaml', 'r')
    instrucoes = yaml.load(stream, Loader=yaml.FullLoader)

    for dict in instrucoes['SB']:
        if contents['funct3'] == dict['funct3']: inst = dict['name']

    return f"{inst} {_rname(contents['rs1'])}, {_rname(contents['rs2'])}, {_conv_bx(_calc_imm(contents), options)}"


def format_S(contents, options):
    inst = ''
    stream = open('instructions.yaml', 'r')
    instrucoes = yaml.load(stream, Loader=yaml.FullLoader)

    for dict in instrucoes['S']:
        if contents['funct3'] == dict['funct3']: inst = dict['name']

    return f"{inst} {_rname(contents['rs2'])}, {_conv_bx(_calc_imm(contents), options)}({_rname(contents['rs1'])})"