from client import *
import random

server = Server('http://pac.bouillaguet.info/TP4/ElGamal-forgery')

result = server.query('/PK/philippe')

p = result['p']
h = result['h']
g = result['g']
q = p-1


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
	return a, u[0], u[1] #a pgcd, u[0] inv de a dans b, [1] inv de b dans a



server = Server('http://pac.bouillaguet.info/TP4/shifumi-deathmatch')


#Démarre une partie

result = server.query("/insert-coin/philippe")
# print(result)

result = server.query("/start/philippe")

print(result)
foobar = result['foobar']
y = 42
g_y = pow(g, y, p)
h_y = pow(h, y, p)
m = 88275625857605 * h_y

PK = {'p':p, 'g':g, 'h':h}
ciphertext = []
ciphertext.append(g_y)
ciphertext.append(m)
commitment = {'PK':PK, 'ciphertext':ciphertext}
parameters = {'foobar':foobar, 'commitment':commitment}

print(parameters)
try:
	result = server.query("/move", parameters)
	print(result)

except:
	pass

parameters = {'move':'PIERRE', 'k':y, 'barfoo':result['barfoo']}

result = server.query("/result")
print(result)