reg_map = {
    "zero":0, "ra":1, "sp":2, "gp":3, "tp":4,
    "t0":5, "t1":6, "t2":7,
    "s0":8, "s1":9,
    "a0":10, "a1":11, "a2":12, "a3":13,
    "a4":14, "a5":15, "a6":16, "a7":17,
    "s2":18, "s3":19, "s4":20, "s5":21,
    "s6":22, "s7":23, "s8":24, "s9":25,
    "s10":26, "s11":27,
    "t3":28, "t4":29, "t5":30, "t6":31
}

def u_type(instruct, register, num):
    opcode = {"lui": "0110111", "auipc": "0010111"}

    if(num < 0):
        num = (1 << 20) + num

    binary_num = format(num, "020b")
    binary_reg = format(reg_map[register], "05b")
    print(binary_num + binary_reg + opcode[instruct])

# instruct, register, num = "lui", "s0", 1
# u_type(instruct, register, num)

def encode_jal(PC, rd_name, offset):
    opcode = "1101111"
    rd = format(reg_map[rd_name], "05b")

    imm21 = offset
    if(imm21 < 0):
        imm21 = (1 << 21) + imm21

    imm_bits = format(imm21, "021b")  

    imm20     = imm_bits[0]
    imm10_1   = imm_bits[10:20]   
    imm11     = imm_bits[9]       
    imm19_12  = imm_bits[1:9]    

    imm_encoded = imm20 + imm10_1 + imm11 + imm19_12  

    print(imm_encoded + rd + opcode)

def j_type(lines):
    PC = 0
    labels = {}
    for line in lines:
        if ":" in line:
            label = line.split(":")[0].strip()
            labels[label] = PC
            # remove label part for instruction counting
            rest = line.split(":", 1)[1].strip()
            if(rest != ""):
                PC += 4
        else:
            PC += 4

    PC = 0
    for line in lines:
        if(":" in line):
            line = line.split(":", 1)[1].strip()
            if(line == ""):
                continue

        parts = line.replace(",", " ").split()

        if(parts[0] == "jal"):
            rd_name = parts[1]
            target = parts[2]

            if(target not in labels):
                print(f"Error: unknown label '{target}' at PC={PC}")
                return

            offset = labels[target] - PC
            encode_jal(PC, rd_name, offset)

        PC += 4

with open("a.out", "r") as f:
    lines = f.readlines()
    for line in lines:
        if(line == ""):
            continue

    lines = [line.strip() for line in lines]
   
j_type(lines)