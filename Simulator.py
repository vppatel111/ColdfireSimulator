import sys

mem = []
data = {}
address = {}

# initialize memory and data address registers to 0
for i in range(256):  # 8 bit operating system
    mem.append(0)
    data["d" + str(i)] = 0
    address["a" + str(i)] = 0

for line in sys.stdin:

    line = line.strip()

    if line == ".end":  # Assembler directive quit.
        sys.exit()
