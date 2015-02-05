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


def enc_rsa(msg, pk_file):
    args = ["openssl", "pkeyutl", "-encrypt", "-pubin", "-inkey", pk_file]
    result = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = result.communicate(msg.encode(ENCODING))
    args = ["base64"]
    result = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = result.communicate(stdout)
    return stdout


############### Script ##################


public_key = server_query(BASE_URL +  '/public-key-101/get-PK')
#public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkz8bHLw65rED1AuU1wJl 6P3ppkx743psQi3bNhvVcarJzqXyAdwoJdYYSXxmIqXIlg60uexll5+HFBXeTLaP gS00iP9e+Yd5kORcxK/BraVDql4JP2HBBztlGz51Ch283J5pfIIt2gHCmqLds7c6 2+kF6bsDBKSUb++orY2auhzKwvMomH0rVcjeSpnkDsPu8ediYm2LO7HNqMMGT2OL dsL5Huf+tHEBYjAfUoVVF10nJ938RxpzPXMJXEKl1n/cibiXz5t0TkJKywXWq4va dJoeEm/8mA+lGH7rtwU0XiSWWsqN7jk2NKVHYtB0kESnTwXMHZR4skAbCEayRx2y JwIDAQAB"
"""if public_key != None: 
    f = open('pk2.pub', 'w')
    f.write(public_key)
    f.close()"""

result = enc_rsa("Hi, how are you?", "pk2.pub")
print(result[0])
parameters = {'ciphertext', result[0]}
server_query(BASE_URL + '/public-key-101/submit/philippe', parameters)
