import socket
import random

def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

# Definir endereço IP e porta da máquina 2 (localhost)
IP_MAQUINA2 = '127.0.0.1'
PORTA_MAQUINA2 = 1234

# Solicitar ao usuário que insira a mensagem
mensagem = input("\n\nDigite uma frase: ")

# Solicitar ao usuário que escolha uma opção
print("\n\nOpções:")
print("1 - Enviar sem criptografia")
print("2 - Enviar com criptografia")
opcao = input("\nEscolha uma opção (1 ou 2): ")

# Criar o socket e conectar à máquina 2
client_socket2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket2.connect((IP_MAQUINA2, 3456))

# Enviar a mensagem em ASCII puro
client_socket2.sendall(opcao.encode('ascii'))

# Fechar a conexão
client_socket2.close()

if opcao == '1':
    # Criar o socket e conectar à máquina 2
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP_MAQUINA2, PORTA_MAQUINA2))

    # Enviar a mensagem em ASCII puro
    client_socket.sendall(mensagem.encode('ascii'))

elif opcao == '2':
    chaves_remetente = []  # Vetor para armazenar as chaves geradas

    for _ in range(5):  # Executar o loop 5 vezes

        # Criar o socket e conectar à máquina 2
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((IP_MAQUINA2, PORTA_MAQUINA2))
        
        # Gerar senha_remetente aleatória de 2 a 50
        senha_remetente = random.randint(2, 50)

        # Gerar um número primo aleatório
        primo = random.randint(100, 1000)
        while not is_prime(primo):
            primo = random.randint(100, 1000)
        
        # Enviar o número primo gerado em ASCII puro
        client_socket.sendall(str(primo).encode('ascii'))

        # Receber o número primo menor gerado pelo destinatário
        primo_menor = int(client_socket.recv(1024).decode('ascii'))

        # Expressao 
        resultado = (primo_menor ** senha_remetente) % primo

        # Enviar o resultado para a máquina 2
        client_socket.sendall(str(resultado).encode('ascii'))

        # Receber o resultado em ASCII puro
        resultado_destinatario = int(client_socket.recv(1024).decode('ascii'))

        # Chave
        chave_remetente = (resultado_destinatario ** senha_remetente) % primo
        
        chaves_remetente.append(chave_remetente)  # Adicionar a chave ao vetor de chaves

    # Encontrar a menor chave
    menor_chave = min(chaves_remetente)
    
    # Deixa a chave entre 126 e 32
    while menor_chave > 126:
        menor_chave = menor_chave - 126 + 32

    # Gerar a mensagem criptografada com base na menor chave
    msg_criptografada = ""
    for letra in mensagem:
        valor_letra = ord(letra) + menor_chave
        if valor_letra > 126:
            nova_letra = chr((valor_letra - 126) + 32) #Para os caracteres ficarem entre ASCII 32 e 126
        else:
            nova_letra = chr(valor_letra)
        msg_criptografada += nova_letra
    
    # Enviar a nova mensagem em ASCII puro
    client_socket.sendall(msg_criptografada.encode('ascii'))

    # Imprimir a nova mensagem na tela
    print("\nMensagem criptografada: " + msg_criptografada + "\n")
    
else:
    print("Opção inválida!")

# Fechar a conexão
client_socket.close()
