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



server = Server('http://pac.bouillaguet.info/TP3/PS3')

result = server.query('/PK/philippe')

p = result['p']
g = result['g']
h = result['h']
print(result)

parameters = {'m':42}

result_0 = server.query('/sign/philippe', parameters)


parameters['m'] = 23

result_1 = server.query('/sign/philippe', parameters)


# result[0] = r 
# x = r^-1(m - k * s) mod q
# k = (m0 - m1)(s0 - s1)^-1 mod q

k = (23 - 42)
s = result_0['signature'][1] - result_1['signature'][1]
# print(s)
s_1 = XGCD(s,p)
# print(s_1)
k = (k * s_1[1]) %p
# print(k)

r_1 = XGCD(result_0['signature'][0],p)[1]

x = r_1 * (23 - k*result_0['signature'][1]) % p
# print(x)

print(result_0['signature'][0]%p)
print(pow(g, k, p))

parameters = {'x':x}
result = server.query('/validate/philippe', parameters)

print(result)