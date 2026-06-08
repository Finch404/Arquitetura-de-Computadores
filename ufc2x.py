import memory
from array import array

MPC = 0
MIR = 0

MAR = 0
MDR = 0
PC = 0
MBR = 0
X = 0
Y = 0
H = 0

N = 0
Z = 1

BUS_A = 0
BUS_B = 0
BUS_C = 0

firmware = array('L',[0]) * 512

#MICROPROGRAMA:

#0: INIT
firmware[0] = 0b000000000_100_00110101_001000_001_001 
              #PC = PC + 1; MBR = memory.read_byte(PC) (FETCH); GOTO MBR.
              
#2 - add: X = X + memory[address] 
firmware[2] = 0b000000011_000_00110101_001000_001_001
              #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 3
firmware[3] = 0b000000100_000_00010100_100000_010_010
              #MAR = MBR; MDR = memory.read_word(MAR); GOTO 4
firmware[4] = 0b000000101_000_00010100_000001_000_000
              #H = MDR; GOTO 5
firmware[5] = 0b000000000_000_00111100_000100_000_011              
              #X = H + X; GOTO 0

#6 - mov: memory[address] = X
firmware[6] = 0b000000111_000_00110101_001000_001_001
              #PC = PC + 1; FETCH; GOTO 7
firmware[7] = 0b000001000_000_00010100_100000_000_010
              #MAR = MBR; GOTO 8
firmware[8] = 0b000000000_000_00010100_010000_100_011
              #MDR = X; WRITE_WORD; GOTO 0
              
#9 - goto: GOTO address
firmware[9]  = 0b000001010_000_00110101_001000_001_001
              #PC = PC + 1; FETCH; GOTO 10
firmware[10] = 0b000000000_100_00010100_001000_001_010
              #PC = MBR; FETCH; GOTO MBR

#11 - jz: IF X == 0 GOTO address
firmware[11] =  0b000001100_001_00010100_000000_000_011
                #BUS_C = X; IF BUS_C == 0 GOTO 268 ELSE GOTO 12
firmware[12] =  0b000000000_000_00110101_001000_000_001
                #PC = PC + 1; GOTO 0
firmware[268] = 0b000001001_000_00000000_000000_000_000
                #GOTO 9

#13 - sub: X = X - memory[address]
firmware[13] = 0b000001110_000_00110101_001000_001_001
               #PC = PC + 1; FETCH; GOTO 14
firmware[14] = 0b000001111_000_00010100_100000_010_010
               #MAR = MBR; read; GOTO 15 
firmware[15] = 0b000010000_000_00101000_000001_000_000
               #H = MDR; GOTO 16
firmware[16] = 0b000000000_000_01111110_000100_000_011
               #X = X - H; GOTO 0

#17 - inc: X = X + 1
firmware[17] = 0b000000000_000_00110101_000100_000_011
               #X = X + 1; GOTO 0

#18 - dec: X = X - 1
firmware[18] = 0b000000000_000_00110110_000100_000_011
               #X = X - 1; GOTO 0

#19 - zera: X = 0
firmware[19] = 0b000000000_000_00010000_000100_000_011
               #X = 0; GOTO 0

#20 - add: Y = Y + memory[address] 
firmware[20] = 0b000010101_000_00110101_001000_001_001
              #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 21
firmware[21] = 0b000010110_000_00010100_100000_010_010
              #MAR = MBR; MDR = memory.read_word(MAR); GOTO 22
firmware[22] = 0b000010111_000_00010100_000001_000_000
              #H = MDR; GOTO 23
firmware[23] = 0b000000000_000_00111100_000010_000_100        
              #Y = H + Y; GOTO 0

#24 - sub: Y = Y - memory[address]
firmware[24] = 0b000011001_000_00110101_001000_001_001
               #PC = PC + 1; FETCH; GOTO 25
firmware[25] = 0b000011010_000_00010100_100000_010_010
               #MAR = MBR; read; GOTO 26
firmware[26] = 0b000011011_000_00101000_000001_000_000
               #H = MDR; GOTO 27
firmware[27] = 0b000000000_000_01111110_000010_000_100
               #Y = Y - H; GOTO 0

#28 - inc: Y = Y + 1
firmware[28] = 0b000000000_000_00110101_000010_000_100
               #Y = Y + 1; GOTO 0

#29 - dec: Y = Y - 1
firmware[29] = 0b000000000_000_00110110_000010_000_100
               #Y = Y - 1; GOTO 0

#30 - zera: Y = 0
firmware[30] = 0b000000000_000_00010000_000010_000_100
               #Y = 0; GOTO 0

#31 - mov: memory[address] = Y
firmware[31] = 0b000100000_000_00110101_001000_001_001
              #PC = PC + 1; FETCH; GOTO 32
firmware[32] = 0b000100001_000_00010100_100000_000_010
              #MAR = MBR; GOTO 33
firmware[33] = 0b000000000_000_00010100_010000_100_100
              #MDR = Y; WRITE_WORD; GOTO 0

#34 - jz: IF Y == 0 GOTO address
firmware[34] =  0b000100011_001_00010100_000000_000_100
                #BUS_B = Y; IF ALU == 0 GOTO 291 ELSE GOTO 35
firmware[35] =  0b000000000_000_00110101_001000_000_001
                #PC = PC + 1; GOTO 0
firmware[291] = 0b000001001_000_00000000_000000_000_000
                #GOTO 9

#36 - inc: memory[address] = memory[address] + 1 
firmware[36] = 0b000100101_000_00110101_001000_001_001
              #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 37
firmware[37] = 0b000100110_000_00010100_100000_010_010
              #MAR = MBR; MDR = memory.read_word(MAR); GOTO 38
firmware[38] = 0b000000000_000_00110101_010000_100_000
              #MDR = MDR + 1; memory.write_word(MAR); GOTO 0

#39 - dec: memory[address] = memory[address] - 1 
firmware[39] = 0b000101000_000_00110101_001000_001_001
              #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 40
firmware[40] = 0b000101001_000_00010100_100000_010_010
              #MAR = MBR; MDR = memory.read_word(MAR); GOTO 41
firmware[41] = 0b000000000_000_00110110_010000_100_000
              #MDR = MDR - 1; memory.write_word(MAR); GOTO 0

#42 - zera: memory[address] = 0
firmware[42] = 0b000101011_000_00110101_001000_001_001
              #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 40
firmware[43] = 0b000101100_000_00010100_100000_010_010
              #MAR = MBR; MDR = memory.read_word(MAR); GOTO 41
firmware[44] = 0b000000000_000_00010000_010000_100_000
              #MDR = 0; memory.write_word(MAR); GOTO 0

#45 - madd: memory[address1] = memory[address1] + memory[address2]
firmware[45] = 0b000101110_000_00110101_001000_000_001
              #PC = PC + 1; GOTO 46
firmware[46] = 0b000101111_000_00110101_001000_001_001
              #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 47
firmware[47] = 0b000110000_000_00010100_100000_010_010
              #MAR = MBR; MDR = memory.read_word(MAR); GOTO 48
firmware[48] = 0b000110001_000_00010100_000001_000_000
              #H = MDR; GOTO 49
firmware[49] = 0b000110010_000_00110110_001000_001_001
              #PC = PC - 1; MBR = memory.read_byte(PC) ; GOTO 50
firmware[50] = 0b000110011_000_00010100_100000_010_010              
              #MAR = MBR; MDR = memory.read_word(MAR); GOTO 51
firmware[51] = 0b000110100_000_00111100_010000_100_000
              #MDR = MDR + H; memory.write_word(MAR); GOTO 52
firmware[52] = 0b000000000_000_00110101_001000_000_001
              #PC = PC + 1

#53 - madd: memory[address] = memory[address] + X
firmware[53] = 0b000110110_000_00010100_000001_000_011
              #H = X; GOTO 54
firmware[54] = 0b000110111_000_00110101_001000_001_001
              #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 55
firmware[55] = 0b000111000_000_00010100_100000_010_010
              #MAR = MBR; MDR = memory.read_word(MAR); GOTO 56
firmware[56] = 0b000000000_000_00111100_010000_100_000
              #MDR = MDR + X; memory.write_word(MAR); GOTO 0

#57 - madd: memory[address] = memory[address] + Y
firmware[57] = 0b000111010_000_00010100_000001_000_100
              #H = Y; GOTO 58
firmware[58] = 0b000111011_000_00110101_001000_001_001
              #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 59
firmware[59] = 0b000111100_000_00010100_100000_010_010
              #MAR = MBR; MDR = memory.read_word(MAR); GOTO 60
firmware[60] = 0b000000000_000_00111100_010000_000_000
              #MDR = MDR + Y; GOTO 0

#61 - msub: memory[address1] = memory[address1] - memory[address2]
firmware[61] = 0b000111110_000_00110101_001000_000_001
              #PC = PC + 1; GOTO 62
firmware[62] = 0b000111111_000_00110101_001000_001_001
              #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 63
firmware[63] = 0b001000000_000_00010100_100000_010_010
              #MAR = MBR; MDR = memory.read_word(MAR); GOTO 64
firmware[64] = 0b001000001_000_00010100_000001_000_000
              #H = MDR; GOTO 65
firmware[65] = 0b001000010_000_00110110_001000_001_001
              #PC = PC - 1; MBR = memory.read_byte(PC) ; GOTO 66
firmware[66] = 0b001000011_000_00010100_100000_010_010              
              #MAR = MBR; MDR = memory.read_word(MAR); GOTO 67
firmware[67] = 0b001000100_000_00111111_010000_100_000
              #MDR = MDR - H; memory.write_word(MAR); GOTO 68
firmware[68] = 0b000000000_000_00110101_001000_000_001
              #PC = PC + 1; GOTO 0

#69 - msub: memory[address] = memory[address] - X
firmware[69] = 0b001000110_000_00010100_000001_000_011
              #H = X; GOTO 70
firmware[70] = 0b001000111_000_00110101_001000_001_001
              #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 71
firmware[71] = 0b001001000_000_00010100_100000_010_010
              #MAR = MBR; MDR = memory.read_word(MAR); GOTO 72
firmware[72] = 0b000000000_000_00111111_010000_100_000
              #MDR = MDR - X; memory.write_word(MAR); GOTO 0

#73 - msub: memory[address] = memory[address] - Y
firmware[73] = 0b001001010_000_00010100_000001_000_100
              #H = Y; GOTO 74
firmware[74] = 0b001001011_000_00110101_001000_001_001
              #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 75
firmware[75] = 0b001001100_000_00010100_100000_010_010
              #MAR = MBR; MDR = memory.read_word(MAR); GOTO 76
firmware[76] = 0b000000000_000_00111111_010000_000_000
              #MDR = MDR - Y; GOTO 0

#77 - mmov: memory[address2] = memory[address1]
firmware[77] = 0b001001110_000_00110101_001000_001_001
              #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 78
firmware[78] = 0b001001111_000_00010100_100000_010_010
              #MAR = MBR; MDR = memory.read_word(MAR); GOTO 79
firmware[79] = 0b001010000_000_00010100_000001_000_000
              #H = MDR; GOTO 80
firmware[80] = 0b001010001_000_00110101_001000_001_001
              #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 81
firmware[81] = 0b001010010_000_00010100_100000_000_010
              #MAR = MBR; GOTO 82
firmware[82] = 0b000000000_000_00011000_010000_100_000
              #MDR = H; write_word(MAR); GOTO 0

#83 - mmov: X = memory[address]
firmware[83] = 0b001010100_000_00110101_001000_001_001
              #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 84
firmware[84] = 0b001010101_000_00010100_100000_010_010
              #MAR = MBR; MDR = memory.read_word(MAR); GOTO 85
firmware[85] = 0b001010110_000_00010100_000001_000_000
              #H = MDR; GOTO 86
firmware[86] = 0b000000000_000_00011000_000100_000_011
              #X = H; GOTO 0 

#83 - mmov: Y = memory[address]
firmware[87] = 0b001011000_000_00110101_001000_001_001
              #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 88
firmware[88] = 0b001011001_000_00010100_100000_010_010
              #MAR = MBR; MDR = memory.read_word(MAR); GOTO 89
firmware[89] = 0b001011010_000_00010100_000001_000_000
              #H = MDR; GOTO 90
firmware[90] = 0b000000000_000_00011000_000010_000_100
              #Y = H; GOTO 0              

#91 - mjz: IF memory[address] == 0 GOTO address
firmware[91] = 0b001011100_000_00110101_001000_001_001
              #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 92
firmware[92] = 0b001011101_000_00010100_100000_010_010
              #MAR = MBR; MDR = memory.read_word(MAR); GOTO 93
firmware[93] = 0b001011110_001_00010100_000000_000_000
              #BUS_C = MDR; IF BUS_C == 0 GOTO 350 ELSE GOTO 94
firmware[94] = 0b000000000_000_00110101_001000_000_001
              #PC = PC + 1; GOTO 0
firmware[350] = 0b000001001_000_00000000_000000_000_000
               #GOTO 9

#95 - getb: X = memory[address] byte 0 com PC retornando para Y
firmware[95] = 0b001100000_000_00110101_001000_001_001
              #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 96
firmware[96] = 0b001100001_000_00010100_000010_000_001
              #Y = PC; GOTO 97
firmware[97] = 0b001100010_000_00010100_001000_001_010
              #PC = MBR; MBR = memory.read_byte(PC); GOTO 98
firmware[98] = 0b001100011_000_00010100_000100_000_010
              #X = MBR; GOTO 99
firmware[99] = 0b000000000_000_00010100_001000_000_100
              #PC = Y; GOTO 0

#100 - getb: X = memory[address] byte 1 com PC retornando para Y
firmware[100] = 0b001100101_000_00110101_001000_001_001
               #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 96
firmware[101] = 0b001100110_000_00010100_000010_000_001
               #Y = PC; GOTO 97
firmware[102] = 0b001100111_000_00110101_001000_001_010
               #PC = MBR + 1; MBR = memory.read_byte(PC); GOTO 98
firmware[103] = 0b001101000_000_00010100_000100_000_010
               #X = MBR; GOTO 99
firmware[104] = 0b000000000_000_00010100_001000_000_100
               #PC = Y; GOTO 0

#105 - getb: X = memory[address] byte 2 com PC retornando para Y
firmware[105] = 0b001101010_000_00110101_001000_001_001
               #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 106
firmware[106] = 0b001101011_000_00010100_000010_000_001
               #Y = PC; GOTO 107
firmware[107] = 0b001101100_000_00110101_001000_000_010
               #PC = MBR + 1; GOTO 108
firmware[108] = 0b001101101_000_00110101_001000_001_001
               #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 109
firmware[109] = 0b001101110_000_00010100_000100_000_010
               #X = MBR; GOTO 110
firmware[110] = 0b000000000_000_00010100_001000_000_100
               #PC = Y; GOTO 0

#105 - getb: X = memory[address] byte 2 com PC retornando para Y
firmware[111] = 0b001110000_000_00110101_001000_001_001
               #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 112
firmware[112] = 0b001110001_000_00010100_000010_000_001
               #Y = PC; GOTO 113
firmware[113] = 0b001110010_000_00110101_001000_000_010
               #PC = MBR + 1; GOTO 114
firmware[114] = 0b001110011_000_00110101_001000_000_001
               #PC = PC + 1; GOTO 115
firmware[115] = 0b001110100_000_00110101_001000_001_001
               #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 116
firmware[116] = 0b001110101_000_00010100_000100_000_010
               #X = MBR; GOTO 117
firmware[117] = 0b000000000_000_00010100_001000_000_100
               #PC = Y; GOTO 0

#118 - sr1: X = X >> 1
firmware[118] = 0b000000000_000_10010100_000100_000_011
               #X = X >> 1

#119 - sr1: Y = Y >> 1
firmware[119] = 0b000000000_000_10010100_000100_000_100
               #Y = Y >> 1

#120 - sr1: memory[address] = memory[address] >> 1
firmware[120] = 0b001111001_000_00110101_001000_001_001
               #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 119
firmware[121] = 0b001111010_000_00010100_100000_010_010
               #MAR = MBR; MDR = memory.read_word(MAR); GOTO 120
firmware[122] = 0b000000000_000_10010100_010000_100_000
               #MDR = MDR >> 1; memory.write_word(MAR); GOTO 0

#123 - sl1: X = X << 1
firmware[123] = 0b000000000_000_01010100_000100_000_011
               #X = X << 1

#124 - sl1: Y = Y << 1
firmware[124] = 0b000000000_000_01010100_000010_000_100
               #Y = Y << 1

#125 - sl1: memory[address] = memory[address] >> 1
firmware[125] = 0b001111110_000_00110101_001000_001_001
               #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 124
firmware[126] = 0b001111111_000_00010100_100000_010_010
               #MAR = MBR; MDR = memory.read_word(MAR); GOTO 125
firmware[127] = 0b000000000_000_10010100_010000_100_000
               #MDR = MDR << 1; memory.write_word(MAR); GOTO 0

#128 - sl8: X = X << 8
firmware[128] = 0b000000000_000_11010100_000100_000_011
               #X = X << 8

#129 - sl8: Y = Y << 8
firmware[129] = 0b000000000_000_11010100_000010_000_100
               #Y = Y << 8

#130 - sl8: memory[address] = memory[address] << 8
firmware[130] = 0b010000011_000_00110101_001000_001_001
               #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 131
firmware[131] = 0b010000100_000_00010100_100000_010_010
               #MAR = MBR; MDR = memory.read_word(MAR); GOTO 132
firmware[132] = 0b000000000_000_11010100_010000_100_000
               #MDR = MDR << 8; memory.write_word(MAR); GOTO 0

#133 - sl7: memory[address] = memory[address] << 7
firmware[133] = 0b010000110_000_00110101_001000_001_001
               #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 134
firmware[134] = 0b010000111_000_00010100_100000_010_010
               #MAR = MBR; MDR = memory.read_word(MAR); GOTO 135
firmware[135] = 0b010001000_000_11010100_010000_000_000
               #MDR = MDR << 8; GOTO 136
firmware[136] = 0b000000000_000_10010100_010000_100_000
               #MDR = MDR >> 1; memory.write_word(MAR); GOTO 0

#137 - jeq: IF memory[address1] == memory[address2] GOTO address3
firmware[137] = 0b010001010_000_00110101_001000_001_001
               #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 138
firmware[138] = 0b010001011_000_00010100_100000_010_010
               #MAR = MBR; MDR = memory.read_word(MAR); GOTO 139
firmware[139] = 0b010001100_000_00010100_000001_000_000
               #H = MDR; GOTO 140
firmware[140] = 0b010001101_000_00110101_001000_001_001
               #PC = PC + 1; MBR = memory.read_byte(PC) ; GOTO 141
firmware[141] = 0b010001110_000_00010100_100000_010_010              
               #MAR = MBR; MDR = memory.read_word(MAR); GOTO 142
firmware[142] = 0b010001111_001_00001111_000001_000_000
               #H = MDR ^ H; GOTO 143
firmware[143] = 0b000000000_000_00110101_001000_000_001
               #PC = PC + 1; GOTO 0
firmware[399] = 0b000001001_000_00000000_000000_000_000
               #GOTO 9

#144 - max: IF memory[address1] > memory[address2]: memomry[address3] = 0 ELSE memory[address3] = 1
firmware[144] = 0b010010001_000_00110101_001000_001_001
               #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 145
firmware[145] = 0b010010010_000_00010100_100000_010_010
               #MAR = MBR; MDR = memory.read_word(MAR); GOTO 146
firmware[146] = 0b010010011_000_00010100_000001_000_000
               #H = MDR; GOTO 147
firmware[147] = 0b010010100_000_00110101_001000_001_001
               #PC = PC + 1; MBR = memory.read_byte(PC) ; GOTO 148
firmware[148] = 0b010010101_000_00010100_100000_010_010              
               #MAR = MBR; MDR = memory.read_word(MAR); GOTO 149
firmware[149] = 0b010010110_001_00001111_000001_000_000
               #H = MDR ^ H; GOTO 150
firmware[150] = 0b010010111_000_00001100_010000_000_000
               #MDR = MDR & H; GOTO 151
firmware[151] = 0b010011000_000_00110101_001000_001_001
               #PC = PC + 1; MBR = memory.read_byte(PC); GOTO 152
firmware[152] = 0b000000000_000_00010100_100000_100_010
               #MAR = MBR; memory.write_word(MAR); GOTO 0

#255: HALT
firmware[255] = 0b00000000000000000000000000000000
                #HALT

def read_regs(reg_num):
   global MDR, PC, MBR, X, Y, H, BUS_A, BUS_B
    
   BUS_A = H
    
   if reg_num == 0:
      BUS_B = MDR
   elif reg_num == 1:
      BUS_B = PC
   elif reg_num == 2:
      BUS_B = MBR
   elif reg_num == 3:
      BUS_B = X
   elif reg_num == 4:
      BUS_B = Y
   else:
      BUS_B = 0

def write_regs(reg_bits):
   global MAR, MDR, PC, X, Y, H, BUS_C
 
   if reg_bits & 0b100000:
      MAR = BUS_C
   if reg_bits & 0b010000:
      MDR = BUS_C
   if reg_bits & 0b001000:
      PC = BUS_C
   if reg_bits & 0b000100:
      X = BUS_C
   if reg_bits & 0b000010:
      Y = BUS_C
   if reg_bits & 0b000001:
      H = BUS_C

def alu(control_bits):
   global N, Z, BUS_A, BUS_B, BUS_C
   
   a = BUS_A
   b = BUS_B
   o = 0
   
   shift_bits = control_bits & 0b11000000
   shift_bits = shift_bits >> 6

   control_bits = control_bits & 0b00111111
   
   if control_bits == 0b011000:
      o = a
   elif control_bits == 0b010100:
      o = b
   elif control_bits == 0b011010:
      o = ~a
   elif control_bits == 0b101100:
      o = ~b
   elif control_bits == 0b111100:
      o = a + b
   elif control_bits == 0b111101:
      o = a + b + 1
   elif control_bits == 0b111001:
      o = a + 1
   elif control_bits == 0b110101:
      o = b + 1
   elif control_bits == 0b111111:
      o = b - a
   elif control_bits == 0b110110:
      o = b - 1
   elif control_bits == 0b111011:
      o = -a
   elif control_bits == 0b001100:
      o = a & b
   elif control_bits == 0b011100:
      o = a | b
   elif control_bits == 0b010000:
      o = 0
   elif control_bits == 0b110001:
      o = 1
   elif control_bits == 0b110010:
      o = -1
   elif control_bits == 0b001111:
    o = a ^ b
   
   if o == 0:
      N = 0
      Z = 1
   else:
      N = 1
      Z = 0
   
   if shift_bits == 0b01:
      o = o << 1
   elif shift_bits == 0b10:
      o = o >> 1
   elif shift_bits == 0b11:
      o = o << 8

   BUS_C = o
    
def next_instruction(nextadd, jam):
   global MPC

   if jam == 0b000:
       MPC = nextadd
       return
       
   if jam & 0b001:
       nextadd = nextadd | (Z << 8)
       
   if jam & 0b010:
       nextadd = nextadd | (N << 8)
       
   if jam & 0b100:
       nextadd = nextadd | MBR

   MPC = nextadd

def memory_io(mem_bits):
   global PC, MAR, MDR, MBR
   
   if mem_bits & 0b001:
      MBR = memory.read_byte(PC)
   if mem_bits & 0b010:
      MDR = memory.read_word(MAR)
   if mem_bits & 0b100:
      memory.write_word(MAR, MDR)


def step():
   global MIR, MPC
   
   MIR = firmware[MPC]

   if MIR == 0:
      return False
   
   read_regs( MIR & 0b00000000000000000000000000000111 )
   alu((MIR & 0b00000000000011111111000000000000) >> 12)
   write_regs( (MIR & 0b00000000000000000000111111000000) >> 6)
   memory_io( (MIR & 0b00000000000000000000000000111000) >> 3 )
   next_instruction(MIR >> 23, (MIR & 0b00000000011100000000000000000000) >> 20)

   return True
   
