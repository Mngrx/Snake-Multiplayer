import socket, pickle

HOST = 'localhost'
PORT = 32122

# Create a socket connection.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))

data = ("jorge", [1, [2, 32, 12] ,[13,21, 31, 31], (5,3,1)])
data_pickle = pickle.dumps(data)
s.send(data_pickle)

data_pickle = s.recv(1024)
data = pickle.loads(data_pickle)
print(data)