import re
import asyncio
import vt
import requests
from config import GOOGLE_API_KEY, VIRUSTOTAL_API_KEY

# URL base para la API de Google Safe Browsing
GOOGLE_SAFE_BROWSING_URL = 'https://safebrowsing.googleapis.com/v4/threatMatches:find'

async def verificar_url_con_google_safe_browsing(url):

    payload = {
        'client': {'clientId': "your_client_id", 'clientVersion': "1.0"},
        'threatInfo': {
            'threatTypes': ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            'platformTypes': ["ANY_PLATFORM"],
            'threatEntryTypes': ["URL"],
            'threatEntries': [{'url': url}]
        }
    }
    params = {'key': GOOGLE_API_KEY}
    try:
        response = requests.post(GOOGLE_SAFE_BROWSING_URL, json=payload, params=params)
        result = response.json()
        if 'matches' in result:
            print(f"URL identificada como maliciosa por Google Safe Browsing: {url}")
            return True
        else:
            print(f"URL no detectada como maliciosa por Google Safe Browsing: {url}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error al consultar Google Safe Browsing: {e}")
        return False

async def verificar_url_con_virustotal(url):

    async with vt.Client(VIRUSTOTAL_API_KEY) as client:
        url_id = vt.url_id(url)
        try:
            analysis = await client.get_object_async(f"/urls/{url_id}")
            total_votes = analysis.last_analysis_stats['malicious'] + analysis.last_analysis_stats['suspicious']
            if total_votes > 0:
                print(f"URL identificada como maliciosa por VirusTotal: {url}")
                return True
            else:
                print(f"URL no detectada como maliciosa por VirusTotal: {url}")
                return False
        except vt.error.APIError as e:
            if e.code == "NotFoundError":
                print(f"URL no presente en la base de datos de VirusTotal (considerada segura): {url}")
            else:
                print(f"Error al consultar VirusTotal: {e}")
            return False

async def es_phishing(url):
   
    #Determina si una URL es phishing consultando ambas APIs.
    
    es_maliciosa_google = await verificar_url_con_google_safe_browsing(url)
    es_maliciosa_virustotal = await verificar_url_con_virustotal(url)
    
    return es_maliciosa_google or es_maliciosa_virustotal

    
async def contiene_phishing(mensaje):
    """
    Examina todas las URLs encontradas en el mensaje proporcionado.
    Verifica cada URL contra las APIs de Google Safe Browsing y VirusTotal.
    Retorna True si se detecta alguna URL maliciosa, de lo contrario False.
    """
    urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', mensaje)
    for url in urls:
        if await es_phishing(url):
            return True
    return False
