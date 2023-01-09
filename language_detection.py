import requests
import json
import os
from dotenv import load_dotenv


class Language_Detection:
    """
    Cette classe appelle le service d'analyse de texte d'Azure pour détecter la langue utilisée dans un texte.
    
    Attributes :
        COG_KEY: votre clé API (vous devez l'avoir écrite dans le fichier .env)
        COG_ENDPOINT: votre API endpoint (vous devez l'avoir écrite dans le fichier .env)
        LANGUAGE_RECOGNITION_URI
        HEADERS
        MAX_TXT_SIZE
        MAX_DOC_AMOUNT
    """
    
    def __init__(self):
        load_dotenv()
        self.COG_KEY = os.getenv('COG_KEY')
        self.COG_ENDPOINT = os.getenv('COG_ENDPOINT')
        self.LANGUAGE_RECOGNITION_URI = self.COG_ENDPOINT + "/text/analytics/v3.1/languages"
        self.HEADERS = {
          'Ocp-Apim-Subscription-Key': self.COG_KEY,
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        }
        self.MAX_TXT_SIZE = 5120
        self.MAX_DOC_AMOUNT = 800
        
        
    def detect(self, text: str, id: str):
        '''Utilisez cette fonction pour détecter la langue d'un seul texte
        
        Paramètres :
            text (str):  Le texte dont vous voulez détecter la langue
            id (str):    L'identifiant du texte (si c'est juste pour un test et que votre texte n'a pas d'id, passez juste "1")
        
        Retour : 
            réponse de la requête (response.text)
        '''
        payload = json.dumps({
            "documents": [
              {
                  "id": id,
                "text": self.truncate_big_text(text)
              }
            ]
        })
        response = self.call_api(payload)
        return response
    
    
    def call_api(self, payload):
        '''Pour utiliser cette fonction, vous devez construire votre propre charge utile.
        veuillez noter que les limites sont :
        - 1000 documents par appel
        - 5120 caractères dans un seul document
        - 1 Mo par demande
        - 100 appels par minute

        Paramètres :
        payload (str) : string json avec la structure suivante :
                {
                    "documents": [
                        {"id": id1, "text": text 1},
                        {"id": id2, "text": text2},
                        ...
                        ]
                }
                
        Retour :
            réponse de la requête API (response.text)

        '''   
        response = requests.request("POST", self.LANGUAGE_RECOGNITION_URI, headers=self.HEADERS, data=payload)
        return response.text
    
    
    def get_language_name(self, text: str, id: str):
        '''utilisez cette fonction si vous n'avez besoin que du nom de la langue détectée en anglais

        Paramètres:
            text (str): Le texte dont vous souhaitez détecter la langue
            id (str): L'identifiant du texte (si votre texte n'a pas d'identifiant, passez simplement "1")

        Retour:
            (str) : le nom de la langue détectée en anglais
        '''
        resp = json.loads(self.detect(text, id))
        return resp["documents"][0]["detectedLanguage"]["name"]
    
    
    def get_language_iso(self, text: str, id: str):
        '''utilisez cette fonction si vous n'avez besoin que du nom de la langue détectée au format ISO 639-1
        
        Paramètres:
            text (str): Le texte dont vous souhaitez détecter la langue
            id (str): L'identifiant du texte (si votre texte n'a pas d'identifiant, passez simplement "1")
                                                
        Retour:
            (str): le nom de la langue détectée au format ISO 639-1
        '''
        resp = json.loads(self.detect(text, id))
        return resp["documents"][0]["detectedLanguage"]["iso6391Name"]
    
    
    def truncate_big_text(self, text: str):
        '''Tronque le texte si sa longueur excède MAX_TXT_SIZE
        
        Paramètres:
            text (str): Le texte à tronquer
        '''
        if(len(text) > self.MAX_TXT_SIZE):
            text = text[:self.MAX_TXT_SIZE - 1]
        return text

