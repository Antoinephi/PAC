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

def dec_rsa(msg, sk_file):
    args = ["base64", "--decode"]
    result = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = result.communicate(msg.encode(ENCODING))
    args = ["openssl", "pkeyutl", "-decrypt", "-inkey", sk_file]
    result = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = result.communicate(stdout)
    return stdout

def generate_secret_key():
    args = ['openssl', 'genpkey', '-algorithm', 'RSA', '-pkeyopt', 'rsa_keygen_bits:2048', '-out', 'rsa_sk.pub']
    result = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1) #1 sec sleep to let the system write and close the sk file
    args = ['openssl', 'pkey', '-in', 'rsa_sk.pub', '-pubout', '-out', 'rsa_pk.pub']
    result = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1)


############### Script ##################

#getting public key from server
public_key = server_query(BASE_URL +  '/public-key-101/get-PK')

if public_key != None: 
    f = open('pk2.pub', 'w')
    f.write(public_key)
    f.close()

#Encryption of the message with the given public key
result = enc_rsa("Hi, how are you?", "pk2.pub")

#Sending Encrypted message
parameters = {'ciphertext': result[0].decode('utf-8')}
response = server_query(BASE_URL + '/public-key-101/submit/philippe', parameters)
# print(response)

#generation public key
generate_secret_key()
#Reading public key from file
f = open('rsa_pk.pub', 'r')
pkey = f.read()
f.close()
#Sending public key to server
parameters = {'public-key' : pkey}
response = server_query(BASE_URL + '/public-key-101/query/philippe', parameters)

# print("response : \n", response)

result = dec_rsa(response, "rsa_sk.pub")
# print("result : \n" , result[0].decode('utf-8'))

#Sending magic key to server through GET
response = server_query(BASE_URL + result[0].decode('utf-8'))
# print(response)

############Hybrid Encryption

#Reading public key from file
f = open('rsa_pk.pub', 'r')
pkey = f.read()
f.close()
#Sending public key to server
parameters = {'public-key' : pkey}
response = server_query(BASE_URL + '/public-key-101/hybrid/philippe', parameters)

print(response)

result = dec_rsa(response['session-key'], 'rsa_sk.pub')

secret_key = result[0].decode('utf-8')
# print(secret_key)

result = enc(response['ciphertext'], passphrase=secret_key, decrypt=True)
print(result)

ciphertext = 'philippe, did you know that 4318217343c7aa35452424076bee6c44 ?'
ciphertext = enc(ciphertext, passphrase=secret_key)
print("ciphertext : \n", ciphertext)
secret_key = enc_rsa(secret_key , 'pk2.pub')
secret_key = secret_key[0].decode('utf-8')

print("secret key :\n",secret_key[:-1])

parameters = {'ciphertext': ciphertext,'session-key':secret_key}
print(parameters)
response = server_query(BASE_URL + '/public-key-101/validate', parameters)
print(response)