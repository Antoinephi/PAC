from client import *


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


def rand():
	global next
	next = next * 1103515245 + 12345
	return (next/65536) % 32768

def srand(seed):
	global next
	next = seed

server = Server("http://pac.bouillaguet.info/TP3/rand/")

result = server.query("/challenge/philippe")
iv = result['IV']
print(iv)

# rand() = (next / 2^16) mod 2^15

# next = 2^16*U + L,
u = (iv[0]*pow(2,16))
print(u)
u = u % pow(2,15)
print(u)
res = ''
for i in range(pow(2,16)):
	if iv[1] == u + i:
		res =  i

if res == '':
	for i in range(pow(2,16)):
		if iv[1] == u + pow(2,16) +i:
			res = i

print(res)


