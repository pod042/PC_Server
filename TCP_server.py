import socket
import threading

bind_ip = ""
bind_port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))

server.listen(5)

print(f"[*] Listening on {bind_ip}: {bind_port}")

# Thread para tratar clientes
def handle_client(client_socket):

    while True:
        # Exibe o que o cliente quer enviar
        request = client_socket.recv(1024)

        print(f"[*] Received: {request}")

        # Envia um pacote de volta
        client_socket.send(b"ACK")

        #client_socket.close()

while True:

    client, addr = server.accept()

    print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")

    # Coloca a thread de cliente em ação para tratar dados de entrada
    client_handler = threading.Thread(target=handle_client, args=(client,))
    client_handler.start()



