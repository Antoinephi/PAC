from client import *
import random
server = Server('http://pac.bouillaguet.info/TP4/ElGamal-forgery')

result = server.query('/PK/philippe')

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



p = result['p']
h = result['h']
g = result['g']
q = p-1

c = 42
r = pow(g, 5) % p 
c = random.randrange(q)
while XGCD(c, q)[0] != 1 :
	c = random.randrange(q)

r = (r * (pow(h, c, p))) % p
s = (-r * XGCD(c, q)[1]) % q

m  = (5 * s) % q
parameters = {"m":m, 'signature':(r, s)}

result = server.query('/verify/philippe', parameters)

print(result)