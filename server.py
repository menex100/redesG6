import socket
from __init__ import check_checksum

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 5555))
server_socket.listen(5)

WINDOW_SIZE = 5  # Tamanho da janela deslizante
next_expected_seq_num = 0  # Próximo número de sequência esperado

try:
    while True:
        connection, address = server_socket.accept()
        print("Conexão estabelecida com ", address)

        while True:
            try:
                msg_received = connection.recv(1024)
                if not msg_received:
                    break
                
                check, msg = check_checksum(msg_received.decode('utf-8'))

                if check == 'ACK':
                    seq_num = int(msg.split("\n")[1].split()[0][1:-1])  # Extrair número de sequência
                    if seq_num == next_expected_seq_num:
                        host_and_msg = msg.split("\n")[0]  # Extrair host e mensagem
                        print(f"Mensagem recebida: {host_and_msg}")
                        connection.sendall("ACK".encode("utf-8"))
                        next_expected_seq_num += 1
                else:
                    print("Erro na mensagem recebida. Solicitando retransmissão.")
                    connection.sendall("NAK".encode("utf-8"))

            except socket.timeout:
                print("Timeout. Aguardando retransmissão.")

except KeyboardInterrupt:
    print("\n\nO servidor foi descontinuado!")
    server_socket.close()
