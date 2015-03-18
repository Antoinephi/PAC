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

seed = sys.argv[1]
# print('/challenge/philippe/' + sys.argv[1])
last_byte = {}
last_byte['status'] = ""
while last_byte['status'] != 'OK':
	seed = int(seed) +1
	seed = str(seed)
	print("Seed : " , seed)
	result = server.query('/challenge/philippe/' + seed)

	# print(result)
	iv = result['IV']
	msg = result['ciphertext']
	# print(msg[len(msg)-2:])
	# print(msg)

	result['status'] = ""
	while result['status'] != 'OK' :	
		b = Block.random(16)
		last_block_len = len(msg) - len(str(b))
		blocks = b.hex() + msg[last_block_len:]
		parameters = {'ciphertext':blocks, 'IV':iv}
		# print(parameters)
		try :
			result = server.query('/oracle/philippe', parameters)
			# print(result)
		except :
			print("fail")	


	y = xor(str(b)[len(str(b))-1:].encode(), "01".encode())
	print(base64.b16encode(y).decode())
	print("msg : \n", msg[last_block_len-len(str(b)):last_block_len])
	x = xor(y, msg[last_block_len-len(str(b)):last_block_len].encode())
	x = base64.b16encode(x).decode()
	y = base64.b16encode(y).decode()
	parameters = {"value":x}
	print(parameters)
	try :
		last_byte = server.query("/last-byte/philippe/" + seed, parameters)
		print("last_byte : " ,last_byte)
	except:
		print("fail")

# result['status'] = ""
# while result['status'] != 'OK' :	
# 	b = Block.random(16)
# 	r = xor(0x02.encode(), y.encode())
# 	r = base64.b16encode(r).decode()
# 	b = str(b)
# 	b[len(b)-1] = r
# 	blocks = b.hex() + msg[last_block_len:]
# 	parameters = {'ciphertext':blocks, 'IV':iv}
# 	print(parameters)
# 	try :
# 		result = server.query('/oracle/philippe', parameters)
# 		print(result)
# 	except :
# 		print("fail")


def calcul_octet(octet, seed, y):
	result = server.query('/challenge/philippe/' + seed)
	iv = result['IV']
	msg = result['ciphertext']
	result = {'status': ''}
	while result['status'] != 'OK' :	
		b = Block.random(16)
		r_lb = "{0:02x}".format(octet)
		r = xor(r_lb.encode(), y.encode())
		r = base64.b16encode(r).decode()
		b = str(b)
		b[len(b)-1] = r
		blocks = b.hex() + msg[last_block_len:]
		parameters = {'ciphertext':blocks, 'IV':iv}
		print(parameters)
		try :
			result = server.query('/oracle/philippe', parameters)
			print(result)
		except :
			print("fail")


# calcul_octet(2, seed)