from client import *



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
res = pow(2, 16) * iv[0]
print("{0:02b}".format(res))
