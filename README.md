# Dados_Socket
 
Código envia dados de uma máquina para outra. O programa tem duas opções:
1-	Passar dados em ASCII puro
2-	Passar dados criptografados assimétricamente

No caso de criptografia assimétrica faz 5 cálculos assimétricos de chave e criptografa a mensagem com a menor chave. Caso a chave for maior que 126 ela é recalculada para que o caracter ASCII fique entre '32 = space' e '126 = ~'