# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import urllib.error
import json

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
        opener = urllib.request.FancyURLopener({})
        with opener.open(request, data) as connexion:
            result = connexion.read().decode(ENCODING)
            if connexion.info()['Content-Type'] == "application/json":
                result = json.loads(result)
        return result
     except urllib.error.HTTPError as e:
        print('error while accessing {2} : [{0}] {1}'.format(e.code, e.reason, url))
        print('the server also says: ' + e.read().decode(ENCODING))




parameters = {'login': 'philippe', 'token': '5e13344a408d884f3a182c88227ed0e5'}
reponse = server_query(BASE_URL + '/encryption-101/validate/philippe', parameters)
print(reponse)