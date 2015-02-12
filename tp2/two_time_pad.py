from client import *
import base64

# def xor(a, b):
#    c = bytearray()
#    for x,y in zip(a,b):
#        c.append(x ^ y)
#    return c

server = Server("http://pac.bouillaguet.info/TP2/")

result = server.query('two-time-pad/challenge/philippe/toto')

# print(result)

# a_xor_b = xor(base64.b16decode(result['A']), base64.b16decode(result['B']))