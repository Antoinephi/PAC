from client import *
import random

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



s = Server('http://pac.bouillaguet.info/TP4/shifumi-deathmatch')


#Démarre une partie

result = s.query("/insert-coin/philippe")
# print(result)

result = s.query("/start/philippe")

# print(result)

c = random.randrange(q)
while XGCD(c, q)[0] != 1 :
	c = random.randrange(q)