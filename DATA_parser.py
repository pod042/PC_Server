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

# Input parameters



NUM_OF_BUFFERS = 4


class buffer:
    def __init__(self, id, sample_data):
        self.id = id
        self.sample_data = sample_data



with open('teste_file.dat', 'rb') as f:
    data = f.read() # Data is an array of bytes
    print(f"Size of data = {len(data)}")

    i = 0
    samples1 = []
    samples2 = []
    samples3 = []
    samples4 = []

    while i < len(data) and i < 1e6:
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

    '''
    print(f'Buffer 1')
    for i in range(len(samples1)):
        print(f'Buffer1[{i}] = {samples1[i]}')

    print(f'Buffer 2')
    for i in range(len(samples2)):
        print(f'Buffer2[{i}] = {samples2[i]}')

    print(f'Buffer 3')
    for i in range(len(samples3)):
        print(f'Buffer3[{i}] = {samples3[i]}')

    print(f'Buffer 4')
    for i in range(len(samples4)):
        print(f'Buffer4[{i}] = {samples4[i]}')
    '''

    print(f"Size of data = {len(data)/1e6} Mbytes")
    
    # Checks for errors
    # Buffer 1
    for i in range(len(samples1)):
        expected = i%800
        if(expected != samples1[i]): 
            print(f"Error found in buffer 1, sample {i}: expected {expected} - recv. {samples1[i]}")
            for n in range(i-5, i+5):
                print(f"Sample {n} - Recv. {samples1[n]}")
            break

    # Buffer 2
    for i in range(len(samples2)):
        expected = i%800 + 100
        if(expected != samples2[i]): 
            print(f"Error found in buffer 2, sample {i}: expected {expected} - recv. {samples2[i]}")
            for n in range(i-5, i+5):
                print(f"Sample {n} - Recv. {samples2[n]}")
            break

    # Buffer 3
    for i in range(len(samples3)):
        expected = i%800 + 200
        if(expected != samples3[i]): 
            print(f"Error found in buffer 3, sample {i}: expected {expected} - recv. {samples3[i]}")
            for n in range(i-5, i+5):
                print(f"Sample {n} - Recv. {samples3[n]}")
            break

    # Buffer 4
    for i in range(len(samples4)):
        expected = i%800 + 300
        if(expected != samples4[i]): 
            print(f"Error found in buffer 4, sample {i}: expected {expected} - recv. {samples4[i]}")
            for n in range(i-5, i+5):
                print(f"Sample {n} - Recv. {samples4[n]}")
            break

    

    




    '''
    while(i < len(data) and i < 10*444):
        # Parses id
        id1 = data[i]
        i+=1
        
        for n in range(0,440,2):
            samples1.append(int.from_bytes(data[i+n:i+n+2], byteorder='big'))
        i+=440
        # Second buffer
        id2 = data[i]
        i+=1
        
        for n in range(0,440,2):
            samples2.append(int.from_bytes(data[i+n:i+n+2], byteorder='big'))
        i+=440
        
        # Third buffer
        id3 = data[i]
        i+=1
        
        for n in range(0,440,2):
            samples3.append(int.from_bytes(data[i+n:i+n+2], byteorder='big'))
        i+=440

        # Fourth buffer
        id4 = data[i]
        i+=1
        
        for n in range(0,440,2):
            samples4.append(int.from_bytes(data[i+n:i+n+2], byteorder='big'))
        i+=440
'''



    '''
    # Reads bytes and parses them
    while data[i] < len(data):
        # Parses id
        id = data[i]
        i+=1
        samples = data[i:i+200]

    '''

