from client import *
import random

server = Server('http://pac.bouillaguet.info/TP4/ElGamal-forgery')

result = server.query('/PK/philippe')

p = result['p']
h = result['h']
g = result['g']
q = p-1


#a^((p-1)/2)
y = 42
g_y = pow(g, y, p)
h_y = pow(h, y, p)
m = (88275625857605 * h_y) % p

g_x = h
g_xy = (g_x * g_y) % p

def legendre(a, p):
	p_1 = (p-1 >> 1)
	a = pow(a, p_1, p)
	print(a)
	return a

legendre(g_xy, p)
reste = (m * g_xy)%p
legendre(reste, p)
# def XGCD(a, b):
# 	u = (1,0)
# 	v = (0,1)
# 	while b != 0:
# 		q, r = divmod(a, b)
# 		a = b
# 		b = r
# 		tmp = (u[0] - q*v[0], u[1] - q*v[1])
# 		u = v
# 		v = tmp
# 	return a, u[0], u[1] #a pgcd, u[0] inv de a dans b, [1] inv de b dans a



# server = Server('http://pac.bouillaguet.info/TP4/shifumi-deathmatch')


# #Démarre une partie

# result = server.query("/insert-coin/philippe")
# # print(result)

# result = server.query("/status/philippe")
# print(result)

# while result['mine'] > 0 or result['yours'] > 0 :

# 	result = server.query("/start/philippe")

# 	# print(result)
# 	foobar = result['foobar']
# 	y = 42
# 	g_y = pow(g, y, p)
# 	h_y = pow(h, y, p)
# 	m = (88275625857605 * h_y) % p

# 	PK = {'p':p, 'g':g, 'h':h}
# 	ciphertext = []
# 	ciphertext.append(g_y)
# 	ciphertext.append(m)
# 	commitment = {'PK':PK, 'ciphertext':ciphertext}
# 	parameters = {'foobar':foobar, 'commitment':commitment}

# 	# print(parameters)
# 	result = server.query("/move", parameters)
# 	# print(result)

# 	parameters = {'move':'PIERRE', 'k':y, 'barfoo':result['barfoo']}

# 	result = server.query("/result", parameters)
# 	print(result['scores'], result['move'])

# 	result = server.query("/status/philippe")
