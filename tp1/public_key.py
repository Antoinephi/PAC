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


def enc_rsa(msg, pk_file,decrypt=False):
    args = ["openssl", "pkeyutl", "-pubin", "-inkey", pk_file]
    if decrypt:
        args.append('-decrypt')
    else:
        args.append('-encrypt')
    result = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = result.communicate(msg.encode(ENCODING))
    args = ["base64"]
    result = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = result.communicate(stdout)
    return stdout

def generate_pk():
    args = ['openssl', 'genpkey', '-algorithm', 'RSA', '-pkeyopt', 'rsa_keygen_bits:2048', '-out', 'rsa_pk.pub']
    result = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = result.communicate(msg.encode(ENCODING))
    if stderr == "bad decrypt\n":
        raise DecryptionError()
    return stdout.decode(ENCODING)

############### Script ##################


public_key = server_query(BASE_URL +  '/public-key-101/get-PK')
#public_key = "MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkz8bHLw65rED1AuU1wJl 6P3ppkx743psQi3bNhvVcarJzqXyAdwoJdYYSXxmIqXIlg60uexll5+HFBXeTLaP gS00iP9e+Yd5kORcxK/BraVDql4JP2HBBztlGz51Ch283J5pfIIt2gHCmqLds7c6 2+kF6bsDBKSUb++orY2auhzKwvMomH0rVcjeSpnkDsPu8ediYm2LO7HNqMMGT2OL dsL5Huf+tHEBYjAfUoVVF10nJ938RxpzPXMJXEKl1n/cibiXz5t0TkJKywXWq4va dJoeEm/8mA+lGH7rtwU0XiSWWsqN7jk2NKVHYtB0kESnTwXMHZR4skAbCEayRx2y JwIDAQAB"
"""if public_key != None: 
    f = open('pk2.pub', 'w')
    f.write(public_key)
    f.close()"""


result = enc_rsa("Hi, how are you?", "pk2.pub")
#encrypton
parameters = {'ciphertext': 'RqCv4uT10N+K3IS+liPdnHcXPWQEjTVCgNK4fHVoQ0mxP6Bx3asCfL5YyTiy8PlHl/TbnGVH80fm\nK6VnAXoBlzGkCreIERC0ojiFi1tYksS93pYtjY0kULq33yvAYCCAl4eGI/pbgwpZhuCsdByz8KGU\ngvi4j8tX2+DvanUfGnGLsOmyVNlwwlOa44+LVYV5+6V/85AEcRzbgGeVfhpz59AzGFfh80Fe8IB9\n/n14L7gBZQWxNvTc5dOPwE0OhWOfDSWOUEplCOWLOM00+pZzqgFQ1tCF7n+D2OxY9ddjgUwdvoFv\nOL6tOURHD13ZOAZalLZgKLfBM+UaRD5/fvyEYw=='}
server_query(BASE_URL + '/public-key-101/submit/philippe', parameters)

f = open('rsa_pk.pub', 'r')
pkey = f.read()
print(pkey)
parameters = {'public-key' : '-----BEGIN PUBLIC KEY-----MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAwB9RSqzqK6A1m6OE/gvoUlpKV+xKOyifDISBXOUnxPQXvLY6RKV/DY1FjtWm/+ezQv1vi2R588ectqkdmiKyN1cyfnPJycMYsuLNLoKSCpkZP2g1udAXn5ROC0W18/xEKZHBbGZZgsajBy1GUVCXX8j77A6SF7jaEN4mQQp5+ld6PKNVO1Ja+IQXe22j673EHsOMWPfVAOPiCXqWi2HFO7rK84psx4J7SruXR0ylGRraFdBERimf8TdQ6nA7FKE+dvNS/E0vxhAJUuNQEvTSlqiIECfRe0X4k0Nc0NtszQeZb5CRhzfQG+PPQCQvs9S9tinCLVWfPoC8HdD620eD1QIDAQAB-----END PUBLIC KEY-----'}
response = server_query(BASE_URL + '/public-key-101/query/philippe', parameters)
print(response)

result = enc_rsa(response, "rsa_pk_.pub", True)
print("result : \n" , result)