import socket
import sys
import threading
import AP
import bitarray


# --- Global variables --- #

# --- General parameters --- #
MAX_SAMPLE_NR = 10

# Global sample bit size table
SAMPLE_BIT_SIZE = [0] * MAX_SAMPLE_NR

# Bytes received
total_bytes_received = 0

# End acq flag
end_acq_flag = False

def access_bit(data, num):
    base = int(num // 8)
    shift = int(num % 8)
    return (data[base] >> shift) & 0x1
            

# Terminal functions
def show_data_size():
    print(f"Received {total_bytes_received} bytes")

def end_acq():
    # Sets flag for end of data acquisition
    global end_acq_flag
    end_acq_flag = True

def create_files():
    # Creates individual .dat files for each sample
    # Globals
    global SAMPLE_BIT_SIZE
    sample_nr = 0
    for i in range(len(SAMPLE_BIT_SIZE)):
        if SAMPLE_BIT_SIZE[i] == 0: break
        sample_nr += 1
        open("sample" + str(i+1) + ".dat", 'w').close() # Resets file

    # Parses through all the data and creates the files
    with open('temp_file.dat', 'rb') as f:
        data_bytes = f.read()
        #data_bits = [access_bit(data_bytes, i) for i in range(len(data_bytes)*8)]
        #data_bits = ''.join(format(ord(byte), '08b') for byte in data_bytes)
        #data_bits.reverse()
        #data_bits = bitstring.Bits(f)
        data_bits = bitarray.bitarray(endian='big')
        data_bits.frombytes(data_bytes)

        #print(f"data_bytes[0:4] = {data_bytes[0:4]}")
        #print(f"data_bits[0:32] = {data_bits[0:32]}")

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
        print(f".dat Files for {sample_nr} samples were created!")

def exit_program():
    global exit_flag
    exit_flag = True


# Terminal command options
terminal_commands = {
    "show data size": show_data_size,
    "end acq": end_acq,
    "create files": create_files,
    "exit program": exit_program
}





# --- TCP/IP server definitions --- #

bind_ip = ""
bind_port = 9999
exit_flag = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



server.bind((bind_ip, bind_port))

server.listen(5)

print(f"[*] Listening on {bind_ip}: {bind_port}")


# Thread para abrir um terminal
def handle_terminal():
    global exit_flag
    while True:
        if exit_flag == True: return
        try:
            cmd = input('Insert input command:')
            try:
                terminal_commands[cmd]()
            except:
                print("Invalid command")
        except:
            print("\nTerminating server")
            exit_flag = True


# Thread para tratar clientes
def handle_client():

    # Global variables
    global total_bytes_received
    global end_acq_flag

    # Private parameters
    SERVER_PARAM_msg = 400
    SERVER_ACK_msg = 500
    SERVER_FAILURE_msg = 600

    client_socket, addr = server.accept()

    # Initialization routine
    message_type = client_socket.recv(32)
    #print(f"Received for config: {message_type}")
    if int.from_bytes(message_type, byteorder='little') == SERVER_PARAM_msg:
        
        # Receives the sample bit size parameters
        data = client_socket.recv(40)
        
        #print(f"Type of data: {type(data)}")
        #print(f"Bit size len: {len(data)}")
        #print(f"Data[0] = {data[0]}")

        # Parses data and saves it in table
        for i in range(len(data)):
            #SAMPLE_BIT_SIZE[i] = int.from_bytes(data[i], byteorder='little')
            SAMPLE_BIT_SIZE[i] = data[i]

        # Prints out received bit size data
        for i in range(len(SAMPLE_BIT_SIZE)):
            print(f"SAMPLE_BIT_SIZE[{i}] = {SAMPLE_BIT_SIZE[i]}")

        # Sends ack back
        client_socket.send(int.to_bytes(SERVER_ACK_msg, 4, byteorder='little'))
    else:
        # Sends failure message back
        client_socket.send(int.to_bytes(SERVER_FAILURE_msg, 4, byteorder='little'))
        return

    while True:

        # Checks flag for end of data acquisiton
        if end_acq_flag == True:
            # Closes socket
            client_socket.close()
            print("Data acquisition stopped!")
            return

        # Saves client data and stores it in a bin file
        client_data = client_socket.recv(110000)

        #print(f"[*] Received data of {len(bytes(client_data))} bytes")
        total_bytes_received += len(bytes(client_data))

        with open("temp_file.dat", "ab+") as f:
            f.write(bytes(client_data))
        
        
def connect_to_AP():
    name = "ESP_AP"
    password = "EMPATHIC_LIGHT"
    AP.createNewConnection(name, name, password)
    while True:
        ret = AP.connect(name, name)
        if ret == 0:
            break
    
    print("Connected to ESP AP!")


def main():
    
    # Resets bin file
    open('temp_file.dat', 'w').close()

    # Tries to connect to ESP AP
    connect_to_AP()
    
    input_terminal = threading.Thread(target=handle_terminal, args=())
    input_terminal.daemon = True
    input_terminal.start()


    client_handler = threading.Thread(target=handle_client, args=())
    client_handler.daemon = True
    client_handler.start()

    while(True):
        if(exit_flag == True):
            sys.exit()



        

if __name__ == '__main__':
    main()

