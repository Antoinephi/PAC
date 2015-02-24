from client import *
import base64



def xor(a, b):
   c = bytearray()
   for x,y in zip(a,b):
       c.append(x ^ y)
   return c


server =  Server('http://pac.bouillaguet.info/TP2')

result = server.query('/two-time-pad/challenge/philippe/23')


a_xor_b = xor(base64.b16decode(result['A'].encode()), base64.b16decode(result['B'].encode()))



print(xor(a_xor_b, '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'.encode()).decode())

print("\n\n--------------------------------------------------\n\n")

print(xor(a_xor_b, '111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111'.encode()).decode())

parameters = {'word':'aperçoit'}
result = server.query('/two-time-pad/answer/philippe/23',parameters)
print(result)
