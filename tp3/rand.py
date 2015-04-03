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
	next = (next * 1103515245 + 12345)% 2**32
	return int((next/65536) % 32768)

def srand(seed):
	global next
	next = seed

def getNext(val):
	a = 1103515245
	b = 12345
	a_1 = XGCD(a, 2**32)
	return int(((val-b)*a_1[1])) % 2**32

def loop(u, iv):
	res = {}
	cursor = 0
	u = u << 16
	u_16 = u + 2**16
	for i in range(0, 2**16):
		val = getNext(u+i)
		val_16 = getNext(u_16+i)
		srand(val)
		rand()
		r = rand()
		if r == iv:
			res[cursor] = val
			cursor+=1
			continue
		val_16 = getNext(u_16+i)
		srand(val_16)
		rand()
		r_16 = rand()
		if r_16 == iv:
			res[cursor] = val_16
			cursor+=1
	return res


server = Server("http://pac.bouillaguet.info/TP3/rand/")

result = server.query("/challenge/philippe")
iv = result['IV']

val = loop(iv[0], iv[1])

result['status'] = ''
cursor = 0
while result['status'] != 'OK' and cursor < 4:
	for i in range(0,4):
		val[cursor] = getNext(val[cursor])

	# srand(val[cursor])

	# for i in range(0,6):
	# 	print(rand())

	srand(val[cursor])

	key = [rand(), rand(), rand(), rand()]
	parameters = {'key':key}

	print(parameters)
	try:
		result = server.query('validation/philippe', parameters)
		print(result)
	except:
		pass
	cursor+=1