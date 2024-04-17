import socket
import time
from __init__ import add_checksum

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 5555))
client_socket.settimeout(2.0)  # Timeout de 2 segundos

WINDOW_SIZE = 5  # Tamanho da janela deslizante
window = []  # Lista para armazenar mensagens na janela
next_seq_num = 0  # Próximo número de sequência a ser enviado

# Solicita o nome do host uma vez no início
host = input("Digite o nome do host: ")

try:
    while True:
        if len(window) < WINDOW_SIZE:
            msg_inputed = input(f"Mensagem [{next_seq_num}]: ")
            msg_seq = f"{host} enviou:\n[{next_seq_num}] {msg_inputed}"
            window.append(msg_seq)
            next_seq_num += 1
        else:
            # Envio das mensagens na janela
            for msg in window:
                client_socket.sendall(add_checksum(msg))
            window = []  # Limpa a janela
            time.sleep(2)  # Tempo para aguardar confirmações

        try:
            confirmation = client_socket.recv(1024)
            print(confirmation.decode("utf-8"))
        except socket.timeout:
            print("Timeout. Reenviando janela.")

except KeyboardInterrupt:
    print("\n\nO cliente encerrou a conexão com o servidor!")
    client_socket.close()
