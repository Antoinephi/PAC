from client import *
from helpers import *
import base64
import sys


def xor(a, b):
   c = bytearray()
   for x,y in zip(a,b):
       c.append(x ^ y)
   return c

server = Server('http://pac.bouillaguet.info/TP2/padding-attack')
# print('/challenge/philippe/' + sys.argv[1])
result = server.query('/challenge/philippe/' + sys.argv[1])

# print(result)
iv = result['IV']
msg = result['ciphertext']
# print(msg[len(msg)-2:])
# print(msg)

b = Block.random(16)
m = Message()
m.append(b.hex())
m.append(msg[384:])
blocks = b.hex()
parameters = {'ciphertext':blocks, 'IV':iv}
print(parameters)
try :
	result = server.query('/oracle/philippe', parameters)
	print(result)
except :
	print('fail')

while result['status'] == 'invalid padding' :	
	b = Block.random(16)
	m = Message()
	m.append(b.hex())
	m.append(msg[384:])
	blocks = b.hex() + msg[384:]
	parameters = {'ciphertext':blocks, 'IV':iv}
	print(parameters)
	try :
		result = server.query('/oracle/philippe', parameters)
		print(result)
	except :
		print("fail")	

# X_pad = int(msg[len(msg)-2:]) ^ int(str(b)[len(msg)-2:])
X_pad = xor(msg[len(msg)-1:].encode(), str(b)[len(str(b))-1:].encode())
# print(base64.b16encode(X_pad).decode)
# X_pad = base64.b16encode(X_pad).decode()
y = xor(str(b)[len(str(b))-1:].encode(), "01".encode())
y = base64.b16encode(y).decode()
print(y)
parameters = {"value":y}
print(parameters)
# result = server.query("/last-byte/philippe/" + sys.argv[1], parameters)
# print(result)