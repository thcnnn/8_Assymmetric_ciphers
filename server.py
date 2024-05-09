import socket
import pickle
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad

HOST = '127.0.0.1'
PORT = 8080
b = 2
sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(1)
conn, addr = sock.accept()
msg = conn.recv(1024)
msg = pickle.loads(msg)
p = msg[0]
g = msg[1]
A = msg[2]
B = pow(g, b, p)
K = pow(A, b, p)
conn.send(pickle.dumps(B))
print('Shared Key (K):', K)

# Дальнейшее общение с использованием симметричного ключа K
cipher = AES.new(K.to_bytes(16, byteorder='big'), AES.MODE_ECB)
while True:
    message = conn.recv(1024)
    decrypted_message = unpad(cipher.decrypt(message), AES.block_size).decode()
    print('Received message:', decrypted_message)

    response = input('Enter response: ')
    encrypted_response = cipher.encrypt(pad(response.encode(), AES.block_size))
    conn.send(encrypted_response)
    if response == '__closeconn':
        conn.close()
        break