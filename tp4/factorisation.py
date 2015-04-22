from client import *
import math
server = Server("http://pac.bouillaguet.info/TP4/factoring/")

def sieve(n):
    np1 = n + 1
    s = list(range(np1)) 
    s[1] = 0
    sqrtn = int(round(n**0.5))
    for i in range(2, sqrtn + 1): 
        if s[i]:
            s[i*i: np1: i] = [0] * len(range(i*i, np1, i))
    return filter(None, s)

premiers = list(sieve(120000000))
# print(premiers)

result = server.query("/get/1/D")
id = result['id']

print(result['n'])

reste = result['n']
liste_diviseurs = []
while(reste not in premiers and reste != 1) :
	for i in premiers:
		if reste % i == 0:
			reste = math.floor(reste / i)
			liste_diviseurs.append(i)
	print(reste)
liste_diviseurs.append(reste)
print(liste_diviseurs)

parameters = {'id':id, 'factors':liste_diviseurs}
result = server.query("submit/philippe", parameters)