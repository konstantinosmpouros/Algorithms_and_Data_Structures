import math
import hashlib
import sys


# Read the data of the file given from the cmd`
def read_data():
    try:
        # save the data in a list
        data = []

        # read the file from the cmd
        with open(sys.argv[1], 'r') as file:
            file = file.read().splitlines()
            for number in file:
                number = int(number)
                data.append(number)
            return data
    except IOError:
        print('Error while reading the data from the file')


# Print the bytes of a bytearray in binary mode with 8 bits
def print_bytearray(byte_array: bytearray):
    for byte in byte_array:
        print(format(byte, '#010b')[2:])


# A method to extract the first l bits of a byte
def extract_first_l_bits(l: int, number: int):
    """
    we just need to have a byte with 8-l zeros and then l one in order to use
    the operator & so we make all the bit 0 after the position l-1. The result
    will be the the first l bits we wanted to take and then 8-l zeros.
    """
    byte = l * '1'
    a = number & int(byte, 2)
    return a


# Create l bytearray method
def create_l(l: int, data: list):
    # Create the l bytearray
    l_bytearray = bytearray()

    '''
    The idea here is the following
    For each number we have read, we take the first l bits from the right. Those bits we will add them in a byte = 1
    by left swifting it each time by l bits and using the operator or (|). Now the byte will be 1 + l bits from the number.
    We are doing this for each number. But when the length of the byte surpasses 9 we must append a byte to the bytearray.
    Why 9? Cause we have one extra bit from the start in the left. There are to chances now in order to append the byte.
    if the length is equal to 9 so the byte will be 1bit + 8bits more and we will append the 8 bits. And the chance to be
    greater than 9 so the byte will be like 1bit + 8bits + more bits. In both chances by right swifting with byte length - 9 
    and using AND with 255 cause 255 in binary is 11111111 so we will take the exact 8 bits we want to append in the bytearray.
    '''
    # The reason that the byte is 1 and not 0 or something else is cause if it was 0 its would be automatically removed,
    # and if tried to append for example 010 the 0 would be removed as well it was bigger we just make our lives harder
    byte = 1
    for i in range(0, len(data)):
        byte = (byte << l) | extract_first_l_bits(l, data[i])
        while byte.bit_length() >= 9:
            l_bytearray.append((byte >> (byte.bit_length() - 9)) & 255)

            '''
            If byte length is equal to 9 that means we appended the 8 bits we wanted so by making byte = 1 we just restart
            the byte from the beginning and its like throwing away the byte we just appended in order to add the new. In the other case the situation is 
            1 bit + 8 bits we appended + more bits. So we just want to keep the 1, remove the 8 bits and keep the rest of the bits in the right.
            So we take again 1, left swifting it the byte length - 9 which is the length of the rest of the bits and by extracting
            those bits from the byte we use OR operator to add them in the left swifted 1 bit. So we end up with 1bit + the rest of the bits.
            '''
            if byte.bit_length() > 9:
                byte = (1 << (byte.bit_length() - 9)) | (byte & int((byte.bit_length() - 9) * '1', 2))
            else:
                byte = 1

    '''
    if the byte length is bigger than 1 that means that the last byte is not completed so we need to add as many
    zeros as to fill the byte. We do 9 - byte length in order to find how many bits are missing and not 8 cause
    we have one extra bit from the start.
    '''
    if byte.bit_length() > 1:
        byte = byte << 9 - byte.bit_length()
        l_bytearray.append(byte & 255)

    return l_bytearray


# Modifying the data list in order to take the numbers of 0 we should add in the U bytearray for every number.
# We just use the >> operator to throw the last l bits of the numbers and then subtract the previous number (i-1)
def modified_first_bits(l: int, data: list):
    # Cutting the last l bits
    for i in range(len(data)):
        data[i] = data[i] >> l

    # Subtract with the previous number. In order to do this without destroying the next subtractions we must read the table upside down
    for i in range(len(data) - 1, 0, -1):
        if i != 0:
            data[i] -= data[i - 1]
    return data


# Creating u bytearray method
def create_u(l: int, data: list):
    # The U bytearray
    u_bytearray = bytearray()

    '''
    The idea here is very simple. The modified first bits is a method that is taking the last remaining bits
    from when we extracted the first l bits to create the l bytearray and is doing the subtraction between n and n-1. 
    So for every number in the modified data list we do (number + 1) left swift. Why +1? Cause the one extra 0 will become one 
    by performing OR (|) operation with 1. So the result will be the byte we had before but at the end we will have number * 0 + 1. 
    Which is what we wanted.
    '''
    byte = 1
    for number in modified_first_bits(l, data):
        byte = (byte << (number + 1)) | 1
        while byte.bit_length() >= 9:
            u_bytearray.append((byte >> (byte.bit_length() - 9)) & 255)

            '''
            If byte length is equal to 9 that means we appended the 8 bits we wanted so by making byte = 1 we just restart
            the byte from the beginning and its like throwing away the byte we just appended in order to add the new. In the other case the situation is 
            1 bit + 8 bits we appended + more bits. So we just want to keep the 1, remove the 8 bits and keep the rest of the bits in the right.
            So we take again 1, left swifting it the byte length - 9 which is the length of the rest of the bits and by extracting
            those bits from the byte we use OR operator to add them in the left swifted 1 bit. So we end up with 1bit + the rest of the bits.
            '''
            if byte.bit_length() > 9:
                byte = (1 << (byte.bit_length() - 9)) | (byte & int((byte.bit_length() - 9) * '1', 2))
            else:
                byte = 1

    '''
    if the byte length is bigger than 1 that means that the last byte is not completed so we need to add as many
    zeros as to fill the byte. We do 9 - byte length in order to find how many bits are missing and not 8 cause
    we have one extra bit from the start.
    '''
    if byte.bit_length() > 1:
        byte = byte << 9 - byte.bit_length()
        u_bytearray.append(byte & 255)

    return u_bytearray


# Printing the results of the algorithm as said in the pdf
def results(l, l_bytearray, u_bytearray, digest):
    print('l ' + str(l))
    print('L')
    print_bytearray(l_bytearray)
    print('U')
    print_bytearray(u_bytearray)
    print(digest)


def main():
    # Read the data
    data = read_data()

    # Calculate l number
    l = math.floor(math.log2(max(data) / len(data)))

    # Create L bytearray
    l_bytearray = create_l(l, data)

    # Create U bytearray
    u_bytearray = create_u(l, data.copy())

    m = hashlib.sha256()
    m.update(l_bytearray)
    m.update(u_bytearray)
    digest = m.hexdigest()

    results(l, l_bytearray, u_bytearray, digest)


if __name__ == "__main__":
    main()
