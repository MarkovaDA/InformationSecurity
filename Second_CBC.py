import First as random
import random as rand


#  +
def read_data(file_path):
    file_reader = open(file_path, "r")
    data = file_reader.read()
    print "Data: '", data, "'\n", "~~~~~~~~~~~~~~~~~~~~~"
    bin_str = ""
    for char in data:
        bin_str += "%08i" % int(bin(ord(char))[2:])
    file_reader.close()
    # print bin_str
    return bin_str


#  +
def generate_blocks(bin_string, length):
    blocks = []
    i = 0
    while i < len(bin_string):
        blocks.append(bin_string[i:i + length])
        i += length

    if len(blocks[len(blocks)-1]) < length:
        zeros = length - len(blocks[len(blocks)-1])
        blocks[len(blocks)-1] += "0"*zeros
    #  print blocks
    return blocks


# +
def bin_str_to_int(str):
    result = int("0b" + str, 2)
    return result


# +
def int_to_bin_str16(number):
    return "%016i" % int(bin(number)[2:])

# +
def int_to_bin_str64(number):
    return "%064i" % int(bin(number)[2:])


# +
def cyclic_shift_right(steps, str):
    index = len(str) - steps
    return str[index:] + str[:index]


# +
def cyclic_shift_left(steps, str):
    return str[steps:] + str[:steps]


# +
def my_not(bin_str):
    str = ""
    for char in bin_str:
        if char == "0":
            str += "1"
        else:
            str += "0"
    return str


def generating_function(block_16bit):
    return bin_str_to_int(my_not(block_16bit))  # [8:16]) + cyclic_shift_left(3, block_16bit[0:8]))


#  +
def generate_key_16bit(key_64bit, index):
    key = cyclic_shift_right(index * 8, key_64bit)[:15]
    key = bin_str_to_int(key)
    return key


# +
def bin64bit_str_to_int_arr(bin_array):
    int_arr = []
    for element in bin_array:
        i = 0
        while i < 64:
            int_arr.append(bin_str_to_int(element[i:i+8]))
            i += 8
    return int_arr


# +
def int_array_to_string(array):
    string = ""
    for element in array:
        string += chr(element)
    return string


def feistel_encryption(file_path, iterations_amount, key_64bit, initial_vector_64bit):
    bin_data = read_data(file_path)
    blocks_64bit = generate_blocks(bin_data, 64)
    blocks_16bit = []  # in the end it will be matrix

    for block in blocks_64bit:
        blocks_16bit.append(generate_blocks(block, 16))
    # print blocks_16bit
    print "len 16 bit blocks = ", len(blocks_16bit)


    result = [initial_vector_64bit]
    j = 0
    for row in blocks_64bit:
        # new_row_str = row[0] + row[1] + row[2] + row[3]
        # print "old row: ", row
        # xor iv
        row_xor_IV = int_to_bin_str64(bin_str_to_int(row) ^ bin_str_to_int(result[j]))
        # print "xor row: ", row_xor_IV
        j += 1

        new_row = []
        i = 0
        while i < 64:
            new_row.append(row_xor_IV[i:i + 16])
            i += 16
        #  print "xor row arr: ", new_row

        # ECB
        for iteration in range(1, iterations_amount+1):
            key_16bit = generate_key_16bit(key_64bit, iteration)  # int key
            key_xor_block3 = bin_str_to_int(new_row[3]) ^ key_16bit  # int
            new_row3 = new_row[2]  # rewrite block3
            new_row2 = int_to_bin_str16(key_xor_block3)  # rewrite block2
            block1_func_xor = generating_function(new_row[1]) ^ key_xor_block3  # int
            new_row1 = new_row[0]  # rewrite block1
            new_row0 = int_to_bin_str16(block1_func_xor)  # rewrite block0

            new_row = [new_row0, new_row1, new_row2, new_row3]
            #print new_row

        new_row_str = new_row[0] + new_row[1] + new_row[2] + new_row[3]
        # print "new row: ", new_row_str
        result.append(new_row_str)

    print "Result: ", result[1::]
    print "len result blocks = ", len(result)-1

    res = bin64bit_str_to_int_arr(result[1::])
    # print "res: ", res
    new_data = int_array_to_string(res)
    # print "New data: '", new_data, "'"
    file_writer = open("output.txt", "w")
    file_writer.write(new_data)
    file_writer.close()


def feistel_decipher(file_path, iterations_amount, key_64bit, initial_vector_64bit):
    bin_data = read_data(file_path)
    blocks_64bit = generate_blocks(bin_data, 64)
    print bin_data
    blocks_16bit = []  # in the end it will be matrix

    for block in blocks_64bit:
        blocks_16bit.append(generate_blocks(block, 16))
    print "blocks 16 bit: ", len(blocks_16bit)


    # initial vector and encrypt data in block by 64bit strings
    encrypt_blocks = [initial_vector_64bit]
    for row in blocks_64bit:
        encrypt_blocks.append(row)  # [0] + row[1] + row[2] + row[3])
    # print "len encrypt blocks = ", len(encrypt_blocks)-1

    # print "encrypt blocks: ", encrypt_blocks

    result = []
    i = 0   # index for array of encrypt data
    for row in blocks_16bit:
        iteration = iterations_amount
        # print "old row: ", row[0] + row[1] + row[2] + row[3]

        new_row = row
        while iteration > 0:
        # for iteration in range(1, iterations_amount+1):
            key_16bit = generate_key_16bit(key_64bit, iteration)  # int key
            # key_16bit = generate_key_16bit(key_64bit, iterations_amount + 1 - iteration)  # int key
            key_xor_block2 = bin_str_to_int(new_row[2]) ^ key_16bit  # int
            block2_xor_block0 = int_to_bin_str16(bin_str_to_int(new_row[0]) ^ bin_str_to_int(new_row[2]))
            new_row0 = new_row[1]  # rewrite block0
            new_row1 = int_to_bin_str16(generating_function(block2_xor_block0))  # rewrite block1
            new_row2 = new_row[3]  # rewrite block2
            new_row3 = int_to_bin_str16(key_xor_block2)  # rewrite block3

            new_row = [new_row0, new_row1, new_row2, new_row3]
            iteration -= 1

        # decrypt data
        new_row_str = new_row[0] + new_row[1] + new_row[2] + new_row[3]
        # decrypt data xor IV
        IV_xor = int_to_bin_str64(bin_str_to_int(new_row_str) ^ bin_str_to_int(encrypt_blocks[i]))
        result.append(IV_xor)
        # print "new row: ", result[i]
        i += 1

    # print "result: ", result
    res = bin64bit_str_to_int_arr(result)
    print "len result blocks = ", len(result)
    print "Result: ", res
    new_data = int_array_to_string(res)
    print "Old data: '", new_data, "'"
    file_writer = open("decipher_input.txt", "w")
    file_writer.write(new_data)
    file_writer.close()


fileinput_path = "inputdata.txt"
fileoutput_path = "output.txt"

iterations_amount = 20  # make depend on sth
keys = random.Random(0.65)
index = rand.randint(0, keys.length-1)
key_64bit = bin(int(keys.numbers[index] * (10**20)))[2:66]
index = rand.randint(0, keys.length-1)
initial_vector = bin(int(keys.numbers[index] * (10**20)))[2:66]

feistel_encryption(fileinput_path, iterations_amount, key_64bit, initial_vector)
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
feistel_decipher(fileoutput_path, iterations_amount, key_64bit, initial_vector)
