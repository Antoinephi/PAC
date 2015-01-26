# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import urllib.error
import json
import time
import subprocess

### adresse du serveur de TP
BASE_URL = "http://pac.bouillaguet.info/TP1"
ENCODING = 'utf-8'

def server_query( url, parameters=None ):
     """Charge l'url demandée. Si aucun paramètre n'est spécifié, une requête
        HTTP GET est envoyée. Si des paramètres sont présents, ils sont encodés
        en JSON, et une requête POST est envoyée.

        La méthode préconisée pour envoyer des paramètres consiste à les stocker
        dans un dictionnaire. Ceci permet de nommer les champs. Par exemple :

        #    sans paramètres
        >>> response = server_query(BASE_URL + '/client-demo')
        >>> print(response)
        Je n'ai pas reçu de paramètres

        #    avec paramètres
        >>> parameters = {'login': 'toto', 'id': 1337}
        >>> response = server_query(BASE_URL + '/client-demo', parameters)
        >>> print(response)
        Dans les paramètres j'ai trouvé :
        *) ``login'' : ``toto''
        *) ``id'' : ``1337''
        <BLANKLINE>
        """
     try:
        request = urllib.request.Request(url)
        data = None
        if parameters is not None:
            data = json.dumps(parameters).encode(ENCODING)
            request.add_header('Content-type', 'application/json')
        with urllib.request.urlopen(request, data) as connexion:
            result = connexion.read().decode(ENCODING)
            if connexion.info()['Content-Type'] == "application/json":
                result = json.loads(result)
        return result
     except urllib.error.HTTPError as e:
        print('error while accessing {2} : [{0}] {1}'.format(e.code, e.reason, url))
        print('the server also says: ' + e.read().decode(ENCODING))


class DecryptionError(Exception):
    pass

def enc(msg, cipher="aes-128-cbc", passphrase=None, base64=True, decrypt=False):
    """invoke the OpenSSL library (though the openssl executable which must be
       present on your system to encrypt or decrypt content using a symmetric cipher."""

    args = ["openssl", "enc", "-" + cipher]
    if base64:
        args.append("-base64")
    if passphrase:
        args.append("-k")
        args.append(passphrase)
    if decrypt:
        args.append('-d')
    result = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = result.communicate(msg.encode(ENCODING))
    if stderr == "bad decrypt\n":
        raise DecryptionError()
    return stdout.decode(ENCODING)


parameters = {'login': 'philippe'}
TGS = server_query(BASE_URL + '/kerberos/AS', parameters)
authen = {'login':'philippe', 'timestamp': time.time()}
ctk = enc(TGS['Client-TGS-key'], passphrase='0abea30252f80c8c841b59aa', decrypt=True)
# print("ctk : " + ctk)
enc_authen = json.dumps(authen)
enc_authen = enc(enc_authen, passphrase=ctk)
req = {'Ticket-Granting-Ticket': TGS['Ticket-Granting-Ticket'], 'server': '248.47.234.160','authenticator': enc_authen}

reponse = server_query(BASE_URL + '/kerberos/TGS', req)

print(reponse)
authen = {'login':'philippe', 'timestamp':time.time()}
enc_authen = json.dumps(authen)
ctk2 = enc(reponse['Client-Server-key'], passphrase=ctk, decrypt=True)
enc_authen = enc(enc_authen, passphrase=ctk2)
parameters = {"Client-to-Server-Ticket":reponse["Client-to-Server-Ticket"], 'authenticator':enc_authen}
reponse = server_query(BASE_URL + '/kerberos/248.47.234.160', parameters)
# print(reponse)

reponse = enc(reponse, passphrase=ctk2, decrypt=True)

print(reponse)

parameters = {'proof':'''U2FsdGVkX18BET4Wc7zUXIzJfmcP3X0ZQgilu5d4Q8GsAGFhrQgKvYyU8nLn6qTK
AH4erPNlGOyY+vPu3YZPTg=='''}
reponse = server_query(BASE_URL + '/kerberos/mission-accomplished', parameters)

print(reponse)

