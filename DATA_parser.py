'''
    This archive is meant to do preliminary tests on the received data from esp32
    It will be organized into an app later on (hopefully)
'''

'''
    Buffer class
        -> id = id number - 1 byte
        -> 
'''

class buffer:
    def __init__(self, id, sample_data):
        self.id = id
        self.sample_data = sample_data



with open('teste_file.dat', 'rb') as f:
    data = f.read() # Data is an array of bytes
    i = 0
    # Parses id
    id1 = data[i]
    i+=1
    samples1 = data[i:i+200]
    i+=200
    # Second buffer
    id2 = data[i]
    i+=1
    samples2 = []
    for n in range(0,400,2):
        samples2.append(int.from_bytes(data[i+n:i+n+2], byteorder='big'))
    i+=400
    
    # Third buffer
    id3 = data[i]
    i+=1
    samples3 = []
    for n in range(0,400,2):
        samples3.append(int.from_bytes(data[i+n:i+n+2], byteorder='big'))
    i+=400

    # Fourth buffer
    id4 = data[i]
    i+=1
    samples4 = []
    for n in range(0,400,2):
        samples4.append(int.from_bytes(data[i+n:i+n+2], byteorder='big'))
    i+=400


print(f'id1 = {id1}')
for i in range(len(samples1)):
    print(f'Buffer1[{i}] = {samples1[i]}')

print(f'id2 = {id2}')
for i in range(len(samples2)):
    print(f'Buffer2[{i}] = {samples2[i]}')

print(f'id3 = {id3}')
for i in range(len(samples3)):
    print(f'Buffer3[{i}] = {samples3[i]}')

print(f'id4 = {id4}')
for i in range(len(samples4)):
    print(f'Buffer4[{i}] = {samples4[i]}')


    '''
    # Reads bytes and parses them
    while data[i] < len(data):
        # Parses id
        id = data[i]
        i+=1
        samples = data[i:i+200]

    '''

