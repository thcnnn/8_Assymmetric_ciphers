import socket
import pickle
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

HOST = '127.0.0.1'
PORT = 8080

sock = socket.socket()
sock.connect((HOST, PORT))

p, g, a = 17, 5, 3
A = pow(g, a, p)
sock.send(pickle.dumps((p, g, A)))
B = pickle.loads(sock.recv(2048))
K = pow(B, a, p)
print('Shared Key (K):', K)

# Дальнейшее общение с использованием симметричного ключа K
cipher = AES.new(K.to_bytes(16, byteorder='big'), AES.MODE_ECB)
while True:
    message = input('Enter message: ')
    encrypted_message = cipher.encrypt(pad(message.encode(), AES.block_size))
    sock.send(encrypted_message)
    response = sock.recv(1024)
    decrypted_response = unpad(cipher.decrypt(response), AES.block_size).decode()
    if decrypted_response == '__closeconn':
        print('server closed connection')
        sock.close()
        break
    print('Received response:', decrypted_response)
    if message == '__quit':
        sock.close()
        break