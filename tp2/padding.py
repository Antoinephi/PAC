from client import *
from helpers import *
import base64


def xor(a, b):
   c = bytearray()
   for x,y in zip(a,b):
       c.append(x ^ y)
   return c

server = Server('http://pac.bouillaguet.info/TP2/padding-attack')

result = server.query('/challenge/philippe/1000')
# print(result)
iv = result['IV']
msg = result['ciphertext']
print(msg[len(msg)-2:])
print(msg)

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
X_pad = xor(base64.b16decode(msg[len(msg)-2:]), base64.b16decode(str(b)[len(msg)-2:]))
print(X_pad)