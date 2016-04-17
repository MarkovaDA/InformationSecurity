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
    # print blocks
    return blocks


# +
def bin_str_to_int(str):
    result = int("0b" + str, 2)
    return result


# +
def int_to_bin_str(number):
    return "%016i" % int(bin(number)[2:])


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
def bin_str_matrix_to_int_arr(bin_array):
    int_arr = []
    for row in bin_array:
        for element in row:
            int_arr.append(bin_str_to_int(element[:8]))
            int_arr.append(bin_str_to_int(element[8:]))
    return int_arr


# +
def int_array_to_string(array):
    string = ""
    for element in array:
        string += chr(element)
    return string


def feistel_encryption(file_path, iterations_amount, key_64bit):
    bin_data = read_data(file_path)
    blocks_64bit = generate_blocks(bin_data, 64)
    blocks_16bit = []  # in the end it will be matrix

    for block in blocks_64bit:
        blocks_16bit.append(generate_blocks(block, 16))
    print "len 16 bit blocks = ", len(blocks_16bit)
    # print blocks_16bit

    blocks = []
    for row in blocks_16bit:
        new_row = row
        # print "old row: ", new_row
        for iteration in range(1, iterations_amount+1):
            key_16bit = generate_key_16bit(key_64bit, iteration)  # int key
            key_xor_block3 = bin_str_to_int(new_row[3]) ^ key_16bit  # int
            new_row3 = new_row[2]  # rewrite block3
            new_row2 = int_to_bin_str(key_xor_block3)  # rewrite block2
            block1_func_xor = generating_function(new_row[1]) ^ key_xor_block3  # int
            new_row1 = new_row[0]  # rewrite block1
            new_row0 = int_to_bin_str(block1_func_xor)  # rewrite block0

            new_row = [new_row0, new_row1, new_row2, new_row3]
            #print new_row
        # print "new row: ", new_row
        blocks.append(new_row)
        # print new_row

    # print blocks
    print "result blocks = ", len(blocks)

    int_blocks = bin_str_matrix_to_int_arr(blocks)
    new_data = int_array_to_string(int_blocks)
    print "New data: '", new_data, "'"
    file_writer = open("output.txt", "w")
    file_writer.write(new_data)
    file_writer.close()


def feistel_decipher(file_path, iterations_amount, key_64bit):
    bin_data = read_data(file_path)
    blocks_64bit = generate_blocks(bin_data, 64)
    blocks_16bit = []  # in the end it will be matrix

    for block in blocks_64bit:
        blocks_16bit.append(generate_blocks(block, 16))
    # print blocks_16bit
    print "le 16 bit blocks = ", len(blocks_16bit)


    blocks = []
    for row in blocks_16bit:
        iteration = iterations_amount
        new_row = row
        #print "old row: ", new_row
        while iteration > 0:
        # for iteration in range(1, iterations_amount+1):
            key_16bit = generate_key_16bit(key_64bit, iteration)  # int key
            # key_16bit = generate_key_16bit(key_64bit, iterations_amount + 1 - iteration)  # int key
            key_xor_block2 = bin_str_to_int(new_row[2]) ^ key_16bit  # int
            block2_xor_block0 = int_to_bin_str(bin_str_to_int(new_row[0]) ^ bin_str_to_int(new_row[2]))
            new_row0 = new_row[1]  # rewrite block0
            new_row1 = int_to_bin_str(generating_function(block2_xor_block0))  # rewrite block1
            new_row2 = new_row[3]  # rewrite block2
            new_row3 = int_to_bin_str(key_xor_block2)  # rewrite block3

            new_row = [new_row0, new_row1, new_row2, new_row3]
            iteration -= 1

        # print "new row: ", new_row
        blocks.append(new_row)
        # print new_row

    # print blocks
    print "result blocks = ", len(blocks)

    int_blocks = bin_str_matrix_to_int_arr(blocks)
    new_data = int_array_to_string(int_blocks)
    print "Old data: '", new_data, "'"
    file_writer = open("decipher_input.txt", "w")
    file_writer.write(new_data)
    file_writer.close()


fileinput_path = "inputdata.txt"
fileoutput_path = "output.txt"

iterations_amount = 20  # make depending on sth
keys = random.Random(0.65)
index = rand.randint(0, keys.length-1)
key_64bit = bin(int(keys.numbers[index] * (10**20)))[2:66]
# print "Key: " + key_64bit

feistel_encryption(fileinput_path, iterations_amount, key_64bit)
print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
feistel_decipher(fileoutput_path, iterations_amount, key_64bit)
