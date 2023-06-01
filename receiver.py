import socket
import random

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Definir endereço IP e porta para receber mensagens (localhost)
IP_MAQUINA2 = '127.0.0.1'
PORTA_MAQUINA1 = 5678
PORTA_MAQUINA2 = 1234

chaves_destinatario = []  # Vetor para armazenar as chaves

# Criar o socket e vincular à máquina 2
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind((IP_MAQUINA2, 3456)) 
s1.listen(1)
print("Aguardando conexão...")

# Aceitar a conexão e receber os dados em ASCII puro
conn1, addr1 = s1.accept()
#print("Conexão estabelecida com", addr)

# Receber os dados em ASCII puro
dados = int(conn1.recv(1024).decode('ascii'))

# Fechar a conexão
conn1.close()
s1.close()

if dados == 1: 
    # Criar o socket e vincular à máquina 2
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP_MAQUINA2, PORTA_MAQUINA2))

    s.listen(1)
    #print("Aguardando conexão...")

    # Aceitar a conexão e receber os dados em ASCII puro
    conn, addr = s.accept()
    #print("Conexão estabelecida com", addr)

    # Receber os dados em ASCII puro
    dados = conn.recv(1024).decode('ascii')
    
    # Dados recebidos são uma frase em ASCII
    mensagem = dados
    print("Frase recebida:", mensagem)

elif dados == 2: 
    for _ in range (5):
        # Criar o socket e vincular à máquina 2
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((IP_MAQUINA2, PORTA_MAQUINA2))
        s.listen(1)
        #print("Aguardando conexão...")

        # Aceitar a conexão e receber os dados em ASCII puro
        conn, addr = s.accept()
        #print("Conexão estabelecida com", addr)

        # Receber os dados em ASCII puro
        dados = conn.recv(1024).decode('ascii')

        # Gerar senha aleatória de 50 a 99
        senha_destinatario = random.randint(50, 99)
        #print("Senha destinatário:", senha_destinatario)

        # Dados recebidos são um número primo
        primo_remetente = int(dados)
        #print("Número primo recebido:", primo_remetente)

        # Gerar um número primo menor que o número recebido
        primo_menor = random.randint(2, primo_remetente - 1)
        while not is_prime(primo_menor):
            primo_menor = random.randint(2, primo_remetente - 1)
    
        #print("Número primo menor gerado:", primo_menor)

        resultado_destinatario = (primo_menor ** senha_destinatario) % primo_remetente
        #print("Resultado da expressão:", resultado_destinatario)

        # Enviar o número primo menor de volta para o remetente
        conn.sendall(str(primo_menor).encode('ascii'))

        # Receber o resultado enviado pelo remetente
        resultado_remetente = int(conn.recv(1024).decode('ascii'))
        #print("Resultado remetente:", resultado_remetente)

        # Enviar o resultado para o remetente
        conn.sendall(str(resultado_destinatario).encode('ascii'))

        # Chave
        chave_destinatario = (resultado_remetente ** senha_destinatario) % primo_remetente
        #print("Chave:", chave_destinatario)

        # Armazenar a chave no vetor
        chaves_destinatario.append(chave_destinatario)

    # Encontrar o valor mínimo
    menor_chave = min(chaves_destinatario)
    #print("Menor chave:", menor_chave)
    while menor_chave > 126:
        menor_chave = menor_chave - 126 + 32

    # Receber os dados em ASCII puro
    msg_criptografada = conn.recv(1024).decode('ascii')
    #print(msg_criptografada)
    # Gerar a nova mensagem com base na menor chave
    msg_descriptografada = ""
    for letra in msg_criptografada:
        valor_letra = ord(letra) - menor_chave
        if valor_letra < 32:
            nova_letra = chr((valor_letra + 126) - 32)
        else:
            nova_letra = chr(valor_letra)
        msg_descriptografada += nova_letra

    # Imprimir a nova mensagem na tela
    print("Mensagem descriptografada:", msg_descriptografada)

# Fechar a conexão
conn.close()
s.close()