import socket, pickle, threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = ''
PORT = 32122

s.bind((HOST, PORT))
s.listen(5)
conn, addr = s.accept()

while True:

	
	data = conn.recv(1024)

	dados = pickle.loads(data)
	print(dados)	
	dados[1].append("Familia")

	data = pickle.dumps(dados)
	s.send(data)
	s.close()