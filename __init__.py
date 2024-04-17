# function to helps parallelism
def handle_client(connection):
    #vamos dizer ao cliente que o sever aceitou a conexão(mandar mensagem)
    mensagem= "conexão aceita"
    connection.sendall(mensagem.encode("utf-8"))

    #recebimento dos pacotes
    while True:
        #recebe msg do cliente
        msg_received = connection.recv(1024)
        check, msg = check_checksum(msg_received.decode('utf-8'))
        #verifica se a msg ta vazia (ctrl+c)
        if msg == "":
            print(f"\nO cliente encerrou a conexao com o servidor!")
            break
    
        #printa msg decodificada
        print(msg)
        print(check)

        #simular erro de timeout
        # time.sleep(3)

        #envia confirmacao que a msg chegou
        msg_to_confirm = "MENSAGEM ENVIADA COM SUCESSO\n"
        #codifica msg de string para bytes
        msg_encoded = msg_to_confirm.encode("utf-8")
        connection.sendall(msg_encoded)

    #estamos encerrando a conexão
    connection.close()


def compute_checksum(data):
    return sum(data) % 256


def add_checksum(data):
    #codifica msg de string para bytes
    checksum = compute_checksum(data.encode("utf-8"))
    return f"{data}|{checksum}".encode("utf-8")


def check_checksum(data):
    if "|" not in data:
        return (None, "")
    msg, checksum = data.rsplit('|', 1)
    #decodifica a msg de bytes para string e verifica
    if compute_checksum(msg.encode("utf-8")) == int(checksum):
        return ('ACK', msg)
    return ('NAK', None)