import urllib
import urllib.parse

import minecraft_launcher_lib
import requests

FALLBACK_PORT = 13372
AUTH_URL="https://login.microsoftonline.com/consumers/oauth2/v2.0/authorize"
TOKEN_URL="https://login.microsoftonline.com/consumers/oauth2/v2.0/token"
SCOPE="XboxLive.signin offline_access"

def getLogin(client_id: str, redirect_uri: str) -> str:
    """
    Generate a login url.\\
    For a more secure alternative, use :func:`get_secure_login_data`                                                      
    :param client_id: The Client ID of your Azure App
    :param redirect_uri: The Redirect URI of your Azure App
    :return: The url to the website on which the user logs in
    """
    parameters = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "response_mode": "query",
        "scope": SCOPE,
    }

    url = urllib.parse.urlparse(AUTH_URL)._replace(query=urllib.parse.urlencode(parameters)).geturl()
    return url

# login_url = getLogin(
#     client_id="76658556-e195-49da-a47e-3c1eb90f6f9b",
#     redirect_uri="http://localhost:13372"
# )
loginurl, state, verifier = minecraft_launcher_lib.microsoft_account.get_secure_login_data(    client_id="ece1bc0c-e3d1-4967-b4a2-63d13c57380c",
    redirect_uri="http://localhost:13372")
print(loginurl)
