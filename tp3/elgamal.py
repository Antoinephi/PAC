from client import *
import random
import math
server = Server("http://pac.bouillaguet.info/TP3/ElGamal-encryption/")
result = server.query("/parameters/philippe")

# print(result)

def XGCD(a, b):
	u = (1,0)
	v = (0,1)
	while b != 0:
		q, r = divmod(a, b)
		a = b
		b = r
		tmp = (u[0] - q*v[0], u[1] - q*v[1])
		u = v
		v = tmp
	return a, u[0], u[1]



g = result['g']
p = result['p']
r = random.randint(1, 42)
# h = g^x
h = pow(g, r, p) 
parameters = {"h": h}
# print(parameters)

result = server.query("/challenge/philippe", parameters)
# print(result)
cipher_a = result['ciphertext'][0]
cipher_b = result['ciphertext'][1]

#h = a^x
h = pow(cipher_a, r, p)

h_1 = XGCD(h, p)
print(h_1)

m =  (h_1[1] * cipher_b) %p

parameters = {"plaintext":m}
print(parameters)
result = server.query("/validate/philippe", parameters)
print(result)