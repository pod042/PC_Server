'''
    This archive is meant to do preliminary tests on the received data from esp32
    It will be organized into an app later on (hopefully)
'''

'''
    Buffer class
        -> id = id number - 1 byte
        -> 
'''

#from ctypes import sizeof
#from nis import match
import struct
#import bitstring
import bitarray

# Input parameters

SAMPLE_BIT_SIZE = [16, 16, 16, 16, 0, 0, 0, 0, 0, 0]

#for i in range(4):
#    open("sample" + str(i+1) + ".dat", 'w').close() # Resets file

def create_files():
    # Creates individual .dat files for each sample
    # Globals
    global SAMPLE_BIT_SIZE
    sample_nr = 0
    for i in range(len(SAMPLE_BIT_SIZE)) and SAMPLE_BIT_SIZE[i] != 0:
        sample_nr += 1
        open("sample" + str(i+1) + ".txt", 'w').close() # Resets file

    # Parses through all the data and creates the files
    with open('temp_file.dat', 'rb') as f:
        data_bytes = f.read()
        #data_bits = [access_bit(data_bytes, i) for i in range(len(data_bytes)*8)]
        #data_bits = ''.join(format(ord(byte), '08b') for byte in data_bytes)
        #data_bits.reverse()
        #data_bits = bitstring.Bits(f)
        data_bits = bitarray.bitarray(endian='big')
        data_bits.frombytes(data_bytes)

        print(f"data_bytes[0:4] = {data_bytes[0:4]}")
        print(f"data_bits[0:32] = {data_bits[0:32]}")

        sample_matrix = [bitarray.bitarray(endian='big') for i in range(sample_nr)]

        sample = 0
        bits_parsed = 0
        while bits_parsed<len(data_bits):
            match sample%sample_nr:
                case 0:
                    sample +=1
                    for i in range(SAMPLE_BIT_SIZE[0]):
                        #sample1.append(struct.pack('?', int(data_bits[bits_parsed], 2)))
                        sample_matrix[0].append((data_bits[bits_parsed]))
                        bits_parsed +=1

                case 1:
                    sample +=1
                    for i in range(SAMPLE_BIT_SIZE[1]):
                        sample_matrix[1].append(((data_bits[bits_parsed])))
                        bits_parsed +=1
                case 2:
                    sample +=1
                    for i in range(SAMPLE_BIT_SIZE[2]):
                        sample_matrix[2].append(((data_bits[bits_parsed])))
                        bits_parsed +=1

                case 3:
                    sample +=1
                    for i in range(SAMPLE_BIT_SIZE[3]):
                        sample_matrix[3].append(((data_bits[bits_parsed])))
                        bits_parsed +=1

        # Writes data to each file
        #print(f"Sample matrix[0][64] = {sample_matrix[0][0:64]}")
        for i in range(sample_nr):
            with open("sample" + str(i+1) + ".dat", "ab+") as f:
                #binary_str = "".join(str(int(x)) for x in sample_matrix[i])
                bytes_to_write = sample_matrix[i].tobytes()
                f.write(bytes_to_write)

def data_parse(sample_nr):
    global SAMPLE_BIT_SIZE
    # Parses through all the data and creates the files
    with open('teste_file.dat', 'rb') as f:
        data_bytes = f.read()
        #data_bits = [access_bit(data_bytes, i) for i in range(len(data_bytes)*8)]
        #data_bits = ''.join(format(ord(byte), '08b') for byte in data_bytes)
        #data_bits.reverse()
        #data_bits = bitstring.Bits(f)
        data_bits = bitarray.bitarray(endian='big')
        data_bits.frombytes(data_bytes)

        print(f"data_bytes[0:4] = {data_bytes[0:4]}")
        print(f"data_bits[0:32] = {data_bits[0:32]}")

        sample_matrix = [bitarray.bitarray(endian='big') for i in range(sample_nr)]

        sample = 0
        bits_parsed = 0
        while bits_parsed<len(data_bits):
            match sample%sample_nr:
                case 0:
                    sample +=1
                    for i in range(SAMPLE_BIT_SIZE[0]):
                        #sample1.append(struct.pack('?', int(data_bits[bits_parsed], 2)))
                        sample_matrix[0].append((data_bits[bits_parsed]))
                        bits_parsed +=1

                case 1:
                    sample +=1
                    for i in range(SAMPLE_BIT_SIZE[1]):
                        sample_matrix[1].append(((data_bits[bits_parsed])))
                        bits_parsed +=1
                case 2:
                    sample +=1
                    for i in range(SAMPLE_BIT_SIZE[2]):
                        sample_matrix[2].append(((data_bits[bits_parsed])))
                        bits_parsed +=1

                case 3:
                    sample +=1
                    for i in range(SAMPLE_BIT_SIZE[3]):
                        sample_matrix[3].append(((data_bits[bits_parsed])))
                        bits_parsed +=1

        # Writes data to each file
        #print(f"Sample matrix[0][64] = {sample_matrix[0][0:64]}")
        for i in range(sample_nr):
            with open("sample" + str(i+1) + ".dat", "ab+") as f:
                #binary_str = "".join(str(int(x)) for x in sample_matrix[i])
                bytes_to_write = sample_matrix[i].tobytes()
                f.write(bytes_to_write)



NUM_OF_BUFFERS = 4

'''
with open('teste_file.dat', 'rb') as f:
    data = f.read() # Data is an array of bytes
    print(f"Size of data = {len(data)}")
    #print(f"Type of data[0] = {type(data[0])}")
    #print(f"bin(data) =")

    i = 0
    samples1 = []
    samples2 = []
    samples3 = []
    samples4 = []

    while i < len(data):
        match ((i/2)%NUM_OF_BUFFERS):
            case 0:
                samples1.append(int.from_bytes(data[i:i+2], byteorder='big'))
                i+=2
            case 1:
                samples2.append(int.from_bytes(data[i:i+2], byteorder='big'))
                i+=2
            case 2:
                samples3.append(int.from_bytes(data[i:i+2], byteorder='big'))
                i+=2
            case 3:
                samples4.append(int.from_bytes(data[i:i+2], byteorder='big'))
                i+=2

    print(f"Size of data = {len(data)/1e6} Mbytes")
    
    # Checks for errors
    # Buffer 1
    errors_flag = 0
    for i in range(len(samples1)):
        expected = i%800
        if(expected != samples1[i]):
            errors_flag = 1
            print(f"Error found in buffer 1, sample {i}: expected {expected} - recv. {samples1[i]}")
            for n in range(i-5, i+5):
                print(f"Sample {n} - Recv. {samples1[n]}")
            break

    # Buffer 2
    for i in range(len(samples2)):
        expected = i%800 + 100
        if(expected != samples2[i]):
            errors_flag = 1
            print(f"Error found in buffer 2, sample {i}: expected {expected} - recv. {samples2[i]}")
            for n in range(i-5, i+5):
                print(f"Sample {n} - Recv. {samples2[n]}")
            break

    # Buffer 3
    for i in range(len(samples3)):
        expected = i%800 + 200
        if(expected != samples3[i]):
            errors_flag = 1
            print(f"Error found in buffer 3, sample {i}: expected {expected} - recv. {samples3[i]}")
            for n in range(i-5, i+5):
                print(f"Sample {n} - Recv. {samples3[n]}")
            break

    # Buffer 4
    for i in range(len(samples4)):
        expected = i%800 + 300
        if(expected != samples4[i]):
            errors_flag = 1
            print(f"Error found in buffer 4, sample {i}: expected {expected} - recv. {samples4[i]}")
            for n in range(i-5, i+5):
                print(f"Sample {n} - Recv. {samples4[n]}")
            break

'''

#data_parse(4)
#create_files()

# Checks for errors
with open('sample1.dat', 'rb') as f:
    data = f.read() # Data is an array of bytes
    print(f"Size of data = {len(data)}")
    #print(f"Type of data[0] = {type(data[0])}")
    #print(f"bin(data) =")

    i = 0
    samples1 = []

    while i < len(data):
        samples1.append(int.from_bytes(data[i:i+2], byteorder='big'))
        i+=2

    print(f"Size of data = {len(data)/1e6} Mbytes")
    
    # Checks for errors
    # Buffer 1
    errors_flag = 0
    for i in range(len(samples1)):
        expected = i%800
        if(expected != samples1[i]):
            errors_flag = 1
            print(f"Error found in buffer 1, sample {i}: expected {expected} - recv. {samples1[i]}")
            for n in range(i-5, i+5):
                print(f"Sample {n} - Recv. {samples1[n]}")
            break

with open('sample2.dat', 'rb') as f:
    data = f.read() # Data is an array of bytes
    print(f"Size of data = {len(data)}")
    #print(f"Type of data[0] = {type(data[0])}")
    #print(f"bin(data) =")

    i = 0
    samples1 = []

    while i < len(data):
        samples1.append(int.from_bytes(data[i:i+2], byteorder='big'))
        i+=2

    print(f"Size of data = {len(data)/1e6} Mbytes")
    
    # Checks for errors
    # Buffer 1
    errors_flag = 0
    for i in range(len(samples1)):
        expected = i%800+100
        if(expected != samples1[i]):
            errors_flag = 1
            print(f"Error found in buffer 1, sample {i}: expected {expected} - recv. {samples1[i]}")
            for n in range(i-5, i+5):
                print(f"Sample {n} - Recv. {samples1[n]}")
            break

with open('sample3.dat', 'rb') as f:
    data = f.read() # Data is an array of bytes
    print(f"Size of data = {len(data)}")
    #print(f"Type of data[0] = {type(data[0])}")
    #print(f"bin(data) =")

    i = 0
    samples1 = []

    while i < len(data):
        samples1.append(int.from_bytes(data[i:i+2], byteorder='big'))
        i+=2

    print(f"Size of data = {len(data)/1e6} Mbytes")
    
    # Checks for errors
    # Buffer 1
    errors_flag = 0
    for i in range(len(samples1)):
        expected = i%800+200
        if(expected != samples1[i]):
            errors_flag = 1
            print(f"Error found in buffer 1, sample {i}: expected {expected} - recv. {samples1[i]}")
            for n in range(i-5, i+5):
                print(f"Sample {n} - Recv. {samples1[n]}")
            break

with open('sample4.dat', 'rb') as f:
    data = f.read() # Data is an array of bytes
    print(f"Size of data = {len(data)}")
    #print(f"Type of data[0] = {type(data[0])}")
    #print(f"bin(data) =")

    i = 0
    samples1 = []

    while i < len(data):
        samples1.append(int.from_bytes(data[i:i+2], byteorder='big'))
        i+=2

    print(f"Size of data = {len(data)/1e6} Mbytes")
    
    # Checks for errors
    # Buffer 1
    errors_flag = 0
    for i in range(len(samples1)):
        expected = i%800+300
        if(expected != samples1[i]):
            errors_flag = 1
            print(f"Error found in buffer 1, sample {i}: expected {expected} - recv. {samples1[i]}")
            for n in range(i-5, i+5):
                print(f"Sample {n} - Recv. {samples1[n]}")
            break


'''
if errors_flag == 0:
    # Cria um arquivo para cada amostra
    open('sample1.txt', 'w').close() # Reseta
    with open('sample1.txt', 'a+') as f:
        for i in range(len(samples1)):
            f.write(str(samples1[i])+"\n")

    # Cria um arquivo para cada amostra
    open('sample2.txt', 'w').close() # Reseta
    with open('sample2.txt', 'a+') as f:
        for i in range(len(samples2)):
            f.write(str(samples2[i])+"\n")

    # Cria um arquivo para cada amostra
    open('sample3.txt', 'w').close() # Reseta
    with open('sample3.txt', 'a+') as f:
        for i in range(len(samples3)):
            f.write(str(samples3[i])+"\n")

    # Cria um arquivo para cada amostra
    open('sample4.txt', 'w').close() # Reseta
    with open('sample4.txt', 'a+') as f:
        for i in range(len(samples4)):
            f.write(str(samples4[i])+"\n")

'''