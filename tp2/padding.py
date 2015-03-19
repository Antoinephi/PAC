from client import *
from helpers import *
import base64
import sys


def xor(a, b):
   c = bytearray()
   for x,y in zip(a,b):
       c.append(x ^ y)
   return c

def last_byte(b, num_bloc, seed):
	last_byte_res = {'status':""}
	# val = "00000000000000{0:02x}".format(num_bloc)

	# """ a surveiller, potentiel bug """
	# b.__ixor__(Block(val.encode()))
	# """ a surveiller, potentiel bug """

	y = xor(str(b)[len(str(b))-1:].encode(), "01".encode())
	y = base64.b16encode(y).decode()
	parameters = {"value":y}
	print(parameters)
	try :
		last_byte = server.query("/last-byte/philippe/" + seed + "/" +num_bloc, parameters)
		print("last_byte : " ,last_byte)
	except:
		print("fail")

	return last_byte_res


def oracle(challenge, num_bloc, dechiffre=None):
	iv = challenge['IV']
	msg = challenge['ciphertext']
	# print(msg)

	msg = Message(challenge['ciphertext'])
	result = {'status':""}
	while result['status'] != 'OK' :
		b = Block.random(16)
		if num_bloc > 1 :
			val = "00000000000000{0:02x}".format(num_bloc)

			""" a surveiller, potentiel bug """
			b.__ixor__(Block(val.encode()))
			""" a surveiller, potentiel bug """

			blocks = b.hex() + msg[len(msg)-1].hex()
		else :
			blocks = b.hex() + msg[len(msg)-1].hex()
		parameters = {'ciphertext':blocks, 'IV':iv}
		# print(parameters)
		result = server.query('/oracle/philippe', parameters)
		# print(result)
	return b	

server = Server('http://pac.bouillaguet.info/TP2/padding-attack')

seed = sys.argv[1]
last_byte_res = {}
last_byte_res['status'] = ""
while last_byte_res['status'] != 'OK':
	seed = int(seed) +1
	seed = str(seed)
	print("Seed : " , seed)
	result = server.query('/challenge/philippe/' + seed)

	b = oracle(result, 1)
	last_byte(b, 1, seed)

	# # print(result)
	# iv = result['IV']
	# msg = result['ciphertext']
	# # print(msg[len(msg)-2:])
	# # print(msg)

	# result['status'] = ""
	# while result['status'] != 'OK' :
	# 	b = Block.random(16)
	# 	last_block_len = len(msg) - len(str(b))
	# 	blocks = b.hex() + msg[last_block_len:]
	# 	parameters = {'ciphertext':blocks, 'IV':iv}
	# 	# print(parameters)
	# 	try :
	# 		result = server.query('/oracle/philippe', parameters)
	# 		# print(result)
	# 	except :
	# 		print("fail")	


	# y = xor(str(b)[len(str(b))-1:].encode(), "01".encode())
	# y = base64.b16encode(y).decode()
	# parameters = {"value":y}
	# print(parameters)
	# try :
	# 	last_byte = server.query("/last-byte/philippe/" + seed, parameters)
	# 	print("last_byte : " ,last_byte)
	# 	dernier_octet = xor(str(b)[len(str(b))-1:].encode(), msg[last_block_len-len(str(b)):last_block_len].encode()) 
	# 	dernier_octet = base64.b16encode(dernier_octet).decode()
	# 	parameters = {"value":y}
	# 	print(parameters)
	# 	# try :
	# 	last_byte = server.query("/last-byte/philippe/" + seed + "/1", parameters)
	# 	print("last_byte : " ,last_byte)			
	# 	# except:
	# 		# print("fail-2")
	# except:
	# 	print("fail")




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


def calcul_octet(octet, seed):
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