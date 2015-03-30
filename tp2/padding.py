from client import *
from helpers import *
import base64
import sys


def last_byte(challenge, b, num_bloc, seed, nb_bloc):
	last_byte_res = {'status':""}
	# val = "00000000000000{0:02x}".format(num_bloc)

	# """ a surveiller, potentiel bug """
	# b.__ixor__(Block(val.encode()))
	# """ a surveiller, potentiel bug """

	iv = challenge['IV']
	msg = Message(challenge['ciphertext'])
	# print(msg[-2])
	# D(K, Y[n]) = r ^ 01
	tmp = Block()
	for i in range(1, num_bloc+1) :
		tmp[-i] = num_bloc
	# print(tmp)
	d_y_n = b.__xor__(tmp)
	#X[n] = D(K, Y[n]) ^ Y[n-1]
	x_n = msg[-nb_bloc-1].__xor__(d_y_n)
	# print(-nb_bloc-1)
	if num_bloc > 1 and nb_bloc == 1:
		x_n = x_n.hex()[-2*num_bloc:(-2*num_bloc)+2]
	else :
		x_n = x_n.hex()[-2:]
	parameters = {"value":x_n}
	print(parameters)
	print("num_bloc : ", num_bloc)
	# print("/last-byte/philippe/" + seed + "/" + str(num_bloc))
	# try :
	# last_byte_res = server.query("/last-byte/philippe/" + seed + "/" +str(num_bloc), parameters)
	# print("last_byte : " ,last_byte_res)
	# except:
		# print("fail")

	return d_y_n, x_n


def oracle(challenge, num_bloc, nb_bloc, dechiffre=None):
	iv = challenge['IV']
	msg = challenge['ciphertext']
	msg = Message(msg)
	# print(msg)
	# print(msg[-2:-1])
	result = {'status':""}
	while result['status'] != 'OK' :
		b = Block.random(16)
		if num_bloc > 1 and nb_bloc == 1:
			val = Block()
			# print("val 0 ", val)
			for i in range(1, num_bloc):
				val[-i] = num_bloc
			# print("val 02 ", val)
			""" a surveiller, potentiel bug """
			val.__ixor__(dechiffre)
			""" a surveiller, potentiel bug """
			# print("dechiffre : ", dechiffre)
			# print("val xor ", val)
			for i in range(1, num_bloc):
				b[-i] = val[-i]
		blocks = b.hex() + msg[-nb_bloc].hex()
		# print(b)
		parameters = {'ciphertext':blocks, 'IV':iv}
		# print(parameters)
		result = server.query('/oracle/philippe', parameters)
		# print(result)
	return b	
server = Server('http://pac.bouillaguet.info/TP2/padding-attack')

seed = sys.argv[1]
j = 0
result = server.query('/challenge/philippe/' + seed)
f = open('blocs_dechiffre_' + str(seed), 'a')
f.write('nb_bloc : '+ str(j) + " " +  "toto" + '\n')

# b = oracle(result, 1, 1)
# d_y_n, x_n = last_byte(result, b, 1, seed, 1)
# bloc.append(x_n)
d_y_n = ""
for j in range(1, 3):
	bloc = []
	b = oracle(result, 1, j, d_y_n)
	d_y_n, x_n = last_byte(result, b, 1, seed, j)
	bloc.append(x_n)
	for i in range(2, 17):
		
		b = oracle(result, i, j,d_y_n)
		d_y_n, x_n = last_byte(result, b, i, seed, j)
		bloc.append(x_n)

	bloc.reverse()
	bloc = ''.join(bloc)
	f.write('nb_bloc : '+ str(j) + " " +  bloc + '\n')
	print("final result : ", bloc)
# parameters = {"value":bloc}
# result = server.query("/last-block/philippe/" + str(seed), parameters)
# print(result)

f.close()
