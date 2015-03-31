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
q = p -1
# print(result)
m0 = 23
m1 = 100

parameters = {'m' : m0}

result_0 = server.query('/sign/philippe', parameters)


parameters['m'] = m1

result_1 = server.query('/sign/philippe', parameters)


# result[0] = r 
# x = r^-1(m - k * s) mod q
# k = (m0 - m1)(s0 - s1)^-1 mod q

s0  = result_0['signature'][1]
s1 = result_1['signature'][1]
r = result_0['signature'][0]
s = s0 - s1

s_1 = XGCD(q, s)

k = ((m0 - m1) * s_1[2]) %q


r_1 = XGCD(r,q)[1]

# x = r^-1(m - k * s) mod q
x = r_1 * (m0 - k*s0) % q
# print(x)

# print(result_0['signature'][0]%p)
# print(pow(g, k, p))

parameters = {'x':x}
result = server.query('/validate/philippe', parameters)

print(result)