from client import *

server = Server('http://pac.bouillaguet.info/TP3/PS3')

result = server.query('/PK/philippe')

print(result)

parameters = {'m':23}

result = server.query('/sign/philippe', parameters)

print(result)

parameters['m'] = 42

result = server.query('/sign/philippe', parameters)

print(result)