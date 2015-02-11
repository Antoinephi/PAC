# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import urllib.error
import json
import time
import subprocess
import os
import binascii
import ast

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


def generate_ecdsa(file):
    args = ['openssl', 'genpkey', '-paramfile', file, '-out', 'secret_key.pem']
    print(args)
    result = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1) #1 sec sleep to let the system write and close the sk file
    args = ['openssl', 'pkey', '-in', 'secret_key.pem', '-pubout', '-out', 'public_key.pem']
    result = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(1)

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

def sign(msg, sk_file):  

    args = ["openssl", "pkeyutl", "-sign", "-inkey", sk_file]
    result = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stdee = result.communicate(msg.encode(ENCODING))
    args = ["base64"]
    result = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = result.communicate(stdout)
    return stdout

############### Script ##################

#Initiating protocol

result = server_query(BASE_URL + '/mutual-authentication/setup/machine-friendly')
random_key = os.urandom(16)
random_key = binascii.b2a_hex(random_key).decode('utf-8')
# print(result)

f = open('rsa_pk.pub', 'r')
rsa_pk = f.read()
f.close()
signed_pk = sign(rsa_pk, 'secret_key.pem')
initiator_public_key = server_query(BASE_URL + '/mutual-authentication/users/' + result['peer'] + '/public-key' )

f = open('initiator_public_key.pem', 'w')
f.write(initiator_public_key['public-key'])
f.close()
# print(initiator_public_key['public-key'])

if result['initiator'] == 'you':

    first_message = {'N_a':random_key, 'login':'philippe'}
    first_message = enc_rsa(str(first_message), 'initiator_public_key.pem')
    print(first_message[0].decode('utf-8'))

    # print(signed_pk.decode('utf-8'))
    parameters = {'public-key':rsa_pk, 'signature':signed_pk.decode('utf-8'), 'A':first_message[0].decode('utf-8')}
    print(parameters)
    result = server_query(BASE_URL + '/mutual-authentication/users/' + result['peer'] + '/step-1', parameters)
    print(result)

else :
    parameters = {'login':'philippe', 'public-key':rsa_pk, 'signature':signed_pk.decode('utf-8')}
    result = server_query(BASE_URL + '/mutual-authentication/users/' + result['peer'] + '/step-0', parameters)
    session_key = dec_rsa(result['A']['session-key'], 'rsa_sk.pub')
    # print(session_key[0].decode('utf-8'))
    cipher = enc(result['A']['ciphertext'], passphrase=session_key[0].decode('utf-8'), decrypt=True)
    cipher = ast.literal_eval(cipher)
    # print(ast.literal_eval(cipher))
    second_message = {'N_a':cipher['N_a'], 'N_b':random_key, 'login':cipher['login']}
    print(second_message)
    second_message = enc_rsa(str(second_message), 'initiator_public_key.pem')
    print(second_message)
    # parameters = {'AB':second_message.decode('utf-8')}
    # print(parameters)
