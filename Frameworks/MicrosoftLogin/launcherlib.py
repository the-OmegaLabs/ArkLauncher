import urllib
import urllib.parse
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

login_url = getLogin(
    client_id="ece1bc0c-e3d1-4967-b4a2-63d13c57380c",
    redirect_uri="http://localhost:13372"
)

print(login_url)