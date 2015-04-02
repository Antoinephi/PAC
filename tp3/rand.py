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



server = Server("http://pac.bouillaguet.info/TP3/rand/")

result = server.query("/challenge/philippe")
iv = result['IV']
print(iv)

# rand() = (next / 2^16) mod 2^15

# next = 2^16*U + L,
u = (iv[0] << 16)

res = ''
ok = {}
cpt = 0
for i in range(0,2**16):
	val = getNext(u + i)
	srand(val)
	rand()
	res = rand()
	if res == iv[1] :
		ok[cpt] = val
		cpt+=1
		print(res)
# if res != iv[1]:
# 	cpt = 0
# 	ok = {}
# 	for i in range(0,2**16):
# 		# u = 2**15 | u
# 		val = getNext(u + 2**16 + i)
# 		# val = getNext(u + 2**16 +  i)
# 		srand(val)
# 		rand()
# 		res = rand()
# 		if res == iv[1] :
# 			ok[cpt] = val
# 			cpt+=1
# 			break
val = ok[1]
for i in range(0,4):
	val = getNext(val)

srand(val)

for i in range(0,6):
	print(rand())


for i in range(0,4):
	srand(val)


	key = [rand(), rand(), rand(), rand()]
	parameters = {'key':key}


	print(parameters)
result = server.query('validation/philippe', parameters)
print(result)
