import socket
import pickle
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
def load_keys(filename):
    with open(filename, "r") as f:
        keys = f.read().strip().split(',')
    return tuple(map(int, keys))

HOST = '127.0.0.1'
PORT = 8080
COMMUNICATION_PORT = 8081
client_keys_file = 'client_keys.txt'

p, g, a = load_keys(client_keys_file)
A = pow(g, a, p)
sock = socket.socket()
sock.connect((HOST, PORT))
sock.send(pickle.dumps((p, g, A)))

B = pickle.loads(sock.recv(2048))
K = pow(B, a, p)
cipher = AES.new(K.to_bytes(16, byteorder='big'), AES.MODE_ECB)
print('Shared Key (K):', K)

sock.close()
sock = socket.socket()
sock.connect((HOST, COMMUNICATION_PORT))

while True:
    message = input('Enter message: ')
    encrypted_message = cipher.encrypt(pad(message.encode(), AES.block_size))
    sock.send(encrypted_message)
    response = sock.recv(1024)
    decrypted_response = unpad(cipher.decrypt(encrypted_message), AES.block_size).decode()
    if decrypted_response == '__closeconn':
        print('Server closed connection')
        sock.close()
        break
    print('Received response:', decrypted_response)
    if message == '__quit':
        sock.close()
        break
