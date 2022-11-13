import socket
import sys
import threading
import AP


# --- Global variables --- #

# --- General parameters --- #
MAX_SAMPLE_NR = 10

# Global sample bit size table
SAMPLE_BIT_SIZE = [0] * MAX_SAMPLE_NR

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
        try:
            cmd = input('Insert input command:')
            print(f"cmd={cmd}")
        except:
            print("\nTerminating server")
            exit_flag = True


# Thread para tratar clientes
def handle_client():

    SERVER_PARAM_msg = 400
    SERVER_ACK_msg = 500
    SERVER_FAILURE_msg = 600

    client_socket, addr = server.accept()

    # Initialization routine
    message_type = client_socket.recv(32)
    print(f"Received for config: {message_type}")
    if int.from_bytes(message_type, byteorder='little') == SERVER_PARAM_msg:
        
        # Receives the sample bit size parameters
        data = client_socket.recv(40)
        
        print(f"Type of data: {type(data)}")
        print(f"Bit size len: {len(data)}")
        print(f"Data[0] = {data[0]}")

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
        # Saves client data and stores it in a bin file
        client_data = client_socket.recv(16384)

        print(f"[*] Received data of {len(bytes(client_data))} bytes")

        with open("teste_file.dat", "ab+") as f:
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
    open('teste_file.dat', 'w').close()

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

