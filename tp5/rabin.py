from client import *

server = Server("http://pac.bouillaguet.info/TP5/Rabin-signature/")

f = open('n.pub', 'r')
n = int(f.read())
parameter = {'n':n}
result = server.query("/challenge/philippe", parameter)
print(result)