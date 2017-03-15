import sys


def toBase(num, conversion):

    if conversion == "HEX":
        print(hex(num))
        return hex(num)
    elif conversion == "OCT":
        print(oct(num))
    else:
        print(bin(num))


def toDecimal(num, conversion):

    if conversion == "HEX":
        print(int(num, base=16))
    elif conversion == "OCT":
        print(int(num, base=8))
    elif conversion == "BIN":
        print(int(num, base=2))


def copyData(register):

    print(register[0:2])

    if register[0:2] == "(A":  # Loads content
        return(address[register[1:3]])  # (A1) 0 1 2 3
    elif register[0] == "D":
        return(data[register])
    elif register[0:3] == "#0x":
        return(int(register[1:], base=16))
    elif register[0:3] == "#0b":
        return(int(register[1:], base=2))
    else:  # Need try-catch
        return(int(register))


def placeData(data_to_store, place_to_store, size):

    if place_to_store[0] == "D":  # Loads content
        temp = data[place_to_store]

        if size == "B":  # Should be removing the last number of digits
            temp = temp & (0b00000000)
            data_to_store = data_to_store & (0b11111111)
        elif size == "W":
            temp = temp & (0b0000000000000000)
            data_to_store = data_to_store & (0b1111111111111111)
        elif size == "L":
            temp = temp & (0b00000000000000000000000000000000)
            data_to_store = data_to_store & (0b11111111111111111111111111111111)

        temp = temp + (data_to_store)  # Replaces the data
        print(temp, data_to_store)

        data[place_to_store] = temp
        print(data[place_to_store])


if __name__ == "__main__":

    mem = []
    data = {}
    address = {}

    # initialize memory and data address registers to 0
    for i in range(256):  # 8 bit operating system
        mem.append(0)
        data["D" + str(i)] = 0b1
        address["A" + str(i)] = 0b1

    for line in sys.stdin:

        line = line.strip()

        if line == ".end":  # Assembler directive quit.
            sys.exit()

        for letter in line:
            line = line.replace(".", " ")
            line = line.replace(",", " ")
            line = line.replace("%", "")

        line = line.split()
        print(line)

        if line[0] == "MOVE":
            if line[1] == "B":
                temp = copyData(line[2])
                placeData(temp, line[3], "B")
                print(temp)
            elif line[1] == "W":
                temp = copyData(line[2])
            elif line[1] == "L":
                temp = copyData(line[2])
