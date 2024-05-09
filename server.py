import socket
import pickle
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
def load_keys(filename):
    with open(filename, "r") as f:
        keys = f.read().strip().split(',')
    return tuple(map(int, keys))

HOST = '127.0.0.1'
PORT = 8080
COMMUNICATION_PORT = 8081
server_keys_file = 'server_keys.txt'

b = load_keys(server_keys_file)[0]

sock = socket.socket()
sock.bind((HOST, PORT))
sock.listen(1)
conn, addr = sock.accept()

msg = conn.recv(1024)
msg = pickle.loads(msg)
p, g, A = msg

B = pow(g, b, p)
K = pow(A, b, p)
conn.send(pickle.dumps(B))
conn.close()
print('Shared Key (K):', K)

sock = socket.socket()
sock.bind((HOST, COMMUNICATION_PORT))
sock.listen(1)
conn, addr = sock.accept()
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
