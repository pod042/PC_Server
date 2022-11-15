
NUM_OF_BUFFERS = 4


with open('temp_file.dat', 'rb') as f:
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
