from client import *
import random
server = Server("http://pac.bouillaguet.info/TP5/RSA-keygen/")

result = server.query("/challenge/philippe")
# print(result)
e = result['e']

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

def maybePrime(n, tries=32):
	for i in range(2, tries):
		if pow(i, n, n) != i:
			return False
	return True

def primeWithE(e, p_q):
	return XGCD(e, p_q)[0] == 1

# print(isPrime())

stop = False
while not stop:
	try :
		p = random.getrandbits(1024)
		while not maybePrime(p) :
			p = random.getrandbits(1024)
		q = random.getrandbits(1024)
		while not maybePrime(q) :
			q = random.getrandbits(1024)

		p_q = (p-1)*(q-1)

		while not primeWithE(e, p_q) :
			p = random.getrandbits(1024)
			while not maybePrime(p) :
				p = random.getrandbits(1024)
			q = random.getrandbits(1024)
			while not maybePrime(q) :
				q = random.getrandbits(1024)	
		n = p*q
		# print(n)
		d = XGCD(e, p_q)[1] % p_q

		parameters = {'n':n, 'e':e}
		result = server.query("/PK/philippe", parameters)
		# print(result)
		if result['ciphertext'] != "":
			stop = True
		c = result['ciphertext']
		m = pow(c, d, n)
		parameters = {'m':m}
		result = server.query("/confirmation/philippe", parameters)
		print(result)
		f = open('e.pub', 'w')
		f.write(str(e))
		f.close()
		f = open('d.pub', 'w')
		f.write(str(d))
		f.close()
		f = open('n.pub', 'w')
		f.write(str(n))
		f.close()
		f = open('p.pub', 'w')
		f.write(str(p))
		f.close()
		f = open('q.pub', 'w')
		f.write(str(q))
		f.close()
	except Exception as ex:
		print(ex)
