import sys

fsrc = open(str(sys.argv[1]), 'r')

lines = []
lines_bin = []
names = []

instructions = ['add', 'sub', 'mov', 'jz', 'inc', 'dec', 'zera',
                'madd', 'msub', 'mmov', 'mjz', 'goto', 'getb',
                'sr1', 'sl1', 'sl8', 'sl7', 'jeq', 'max', 'halt', 'wb', 'ww']

# x, y, mem
instruction_set = {'add' : [0x02, 0x14],
                   'sub' : [0x0D, 0x18],
                   'mov' : [0x06, 0x1F],
                   'jz'  : [0x0B, 0x22], # byte_only
                   'inc' : [0x11, 0x1C, 0x24], # 1op 
                   'dec' : [0x12, 0x1D, 0x27], # 1op 
                   'zera': [0x13, 0x1E, 0x2A], # 1op
                   'madd': [0x2D, 0x35, 0x39],
                   'msub': [0x3D, 0x45, 0x49],
                   'mmov': [0x4D, 0x53, 0x57],
                   'mjz' : 0x5B, # mem1 = word ; mem2 = byte 
                   'goto': 0x09, # byte_only
                   'getb': [0x5F, 0x64, 0x69, 0x6F],
                   'sr1' : [0x76, 0x77, 0x78], # 1op
                   'sl1' : [0x7B, 0x7C, 0x7D], # 1op
                   'sl8' : [0x80, 0x81, 0x82], # 1op
                   'sl7' : 0x85, # mem_only
                   'jeq' : 0x89, # mem1 = word ; mem2 = word ; mem3 = byte
                   'max' : 0x90, # word_only
                   'halt': 0xFF}

byte_only_instructions = [instruction_set['jz'][0], instruction_set['jz'][1],
                          instruction_set['goto'], instruction_set['getb'][0],
                          instruction_set['getb'][1], instruction_set['getb'][2],
                          instruction_set['getb'][3]]

def is_instruction(str):
   global instructions
   inst = False
   for i in instructions:
      if i == str:
         inst = True
         break
   return inst
   
def is_name(str):
   global names
   name = False
   for n in names:
      if n[0] == str:
         name = True
         break
   return name
   
def encode_2ops(inst, ops):
   line_bin = []
   if len(ops) > 1:
      if is_name(ops[1]):
         inst_bin = 0
         if ops[0] == 'x': inst_bin = instruction_set[inst][0]
         elif ops[0] == 'y': inst_bin = instruction_set[inst][1]      
         line_bin.append(inst_bin)
         line_bin.append(ops[1])

   return line_bin
   
def encode_1op(inst, ops):
   line_bin = []
   if len(ops) > 0:
      if ops[0] in ['x', 'y']: #se op é registrador
         inst_bin = 0
         if ops[0] == 'x': inst_bin = instruction_set[inst][0]
         elif ops[0] == 'y': inst_bin = instruction_set[inst][1]
         line_bin.append(inst_bin)

      elif is_name(ops[0]): #se op é endereço de memória
         inst_bin = instruction_set[inst][2]   
         line_bin.append(inst_bin)
         line_bin.append(ops[0])
   return line_bin

def encode_mem_inst(inst, ops):
   line_bin = []
   if len(ops) > 1:
      inst_bin = 0
      if is_name(ops[0]):
         if is_name(ops[1]):
            inst_bin = instruction_set[inst][0]
            line_bin.append(instruction_set[inst][0])
            line_bin.append(ops[0]) # word
            line_bin.append(ops[1]) # word

         elif ops[1] in ['x', 'y']:
            if ops[1] == 'x': inst_bin = instruction_set[inst][1]
            elif ops[1] == 'y': inst_bin = instruction_set[inst][2]
            line_bin.append(inst_bin)
            line_bin.append(ops[0]) # word
   return line_bin

def encode_mjz(ops):
   line_bin = []
   if len(ops) > 1:
      if is_name(ops[0]) and is_name(ops[1]):
         line_bin.append(instruction_set['mjz'])
         line_bin.append(ops[0]) # word
         line_bin.append(ops[1]) # byte
   return line_bin

def encode_goto(ops):
   line_bin = []
   if len(ops) > 0:
      if is_name(ops[0]):
         line_bin.append(instruction_set['goto'])
         line_bin.append(ops[0])
   return line_bin

def encode_getb(ops):
   line_bin = []
   if len(ops) > 1:
      inst_bin = instruction_set['getb'][int(ops[1])]
      if is_name(ops[0]):
         line_bin.append(inst_bin)
         line_bin.append(ops[0])
   return line_bin

def encode_sl7(ops):
   line_bin = []
   if len(ops) > 0:
      if is_name(ops[0]):
         line_bin.append(instruction_set['sl7'])
         line_bin.append(ops[0])
   return line_bin

def encode_jeq(ops):
   line_bin = []
   if len(ops) > 2:
      if is_name(ops[0]) and is_name(ops[1]) and is_name(ops[2]):
         line_bin.append(instruction_set['jeq'])
         line_bin.append(ops[0]) # word
         line_bin.append(ops[1]) # word
         line_bin.append(ops[2]) # byte
   return line_bin

def encode_max(ops):
   line_bin = []
   if len(ops) > 2:
      if is_name(ops[0]) and is_name(ops[1]) and is_name(ops[2]):
         line_bin.append(instruction_set['max'])
         line_bin.append(ops[0]) # word
         line_bin.append(ops[1]) # word
         line_bin.append(ops[2]) # word
   return line_bin

def encode_halt():
   line_bin = []
   line_bin.append(instruction_set['halt'])
   return line_bin
   
def encode_wb(ops):
   line_bin = []
   if len(ops) > 0:
      if ops[0].isnumeric():
         if int(ops[0]) < 256:
            line_bin.append(int(ops[0]))
   return line_bin

def encode_ww(ops):
   line_bin = []
   if len(ops) > 0:
      if ops[0].isnumeric():
         val = int(ops[0])
         if val < pow(2,32):
            line_bin.append(val & 0xFF)
            line_bin.append((val & 0xFF00) >> 8)
            line_bin.append((val & 0xFF0000) >> 16)
            line_bin.append((val & 0xFF000000) >> 24)
   return line_bin
      
def encode_instruction(inst, ops):
   if inst in ['add', 'sub', 'mov', 'jz']:
      return encode_2ops(inst, ops)
   elif inst in ['inc', 'dec', 'zera', 'sr1', 'sl1', 'sl8']:
      return encode_1op(inst, ops)
   elif inst in ['madd', 'msub', 'mmov']:
      return encode_mem_inst(inst, ops)
   elif inst == 'mjz':
      return encode_mjz(ops)
   elif inst == 'goto':
      return encode_goto(ops)
   elif inst == 'getb':
      return encode_getb(ops)
   elif inst == 'sl7':
      return encode_sl7(ops)
   elif inst == 'jeq':
      return encode_jeq(ops)
   elif inst == 'max':
      return encode_max(ops)
   elif inst == 'halt':
      return encode_halt()
   elif inst == 'wb':
      return encode_wb(ops)
   elif inst == 'ww':
      return encode_ww(ops)
   else:
      return []
   
def line_to_bin_step1(line):
   line_bin = []
   if is_instruction(line[0]):
      line_bin = encode_instruction(line[0], line[1:])
   else:
      line_bin = encode_instruction(line[1], line[2:])
   return line_bin
   
def lines_to_bin_step1():
   global lines
   for line in lines:
      line_bin = line_to_bin_step1(line)
      if line_bin == []:
         print("Erro de sintaxe na linha ", lines.index(line))
         return False
      lines_bin.append(line_bin)
   return True

def find_names():
   global lines
   for k in range(0, len(lines)):
      is_label = True
      for i in instructions:
          if lines[k][0] == i:
             is_label = False
             break
      if is_label:
         names.append((lines[k][0], k))
         
def count_bytes(line_number):
   line = 0
   byte = 1
   while line < line_number:
      byte += len(lines_bin[line])
      line += 1
   return byte

def get_name_byte(str):
   for name in names:
      if name[0] == str:
         return name[1]
         
def resolve_names():
   for i in range(0, len(names)):
      names[i] = (names[i][0], count_bytes(names[i][1]))
   for line in lines_bin:
      for i in range(0, len(line)):
         if is_name(line[i]):

            if line[0] == instruction_set['mjz']:
               if i == 1: line[i] = get_name_byte(line[i])//4 # word
               elif i == 2: line[i] = get_name_byte(line[i]) # byte
            
            elif line[0] == instruction_set['jeq']:
               if i == 1 or i == 2: line[i] = get_name_byte(line[i])//4 # word
               elif i == 3: line[i] = get_name_byte(line[i]) # byte

            elif line[0] == instruction_set['max']:
               line[i] = get_name_byte(line[i])//4 # word

            elif line[0] in byte_only_instructions:
               line[i] = get_name_byte(line[i])
            else:
               line[i] = get_name_byte(line[i])//4

for line in fsrc:
   tokens = line.replace('\n','').replace(',','').lower().split(" ")
   i = 0
   while i < len(tokens):
      if tokens[i] == '':
         tokens.pop(i)
         i -= 1
      i += 1
   if len(tokens) > 0:
      lines.append(tokens)
   
find_names()
if lines_to_bin_step1():
   resolve_names()
   byte_arr = [0]
   for line in lines_bin:
      for byte in line:
         byte_arr.append(byte)
   fdst = open(str(sys.argv[2]), 'wb')
   fdst.write(bytearray(byte_arr))
   fdst.close()

fsrc.close()
