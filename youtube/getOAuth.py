import os
import dotenv
import pickle

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request, AuthorizedSession
import google_auth_oauthlib
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

dotenv.load_dotenv()
client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
client_secrets_file = os.path.join(root, os.environ["CLIENT_SECRET_FILE"])


def get_credentials(scopes) -> Credentials:
    credentials = google_auth_oauthlib.get_user_credentials(
        scopes, client_id, client_secret
    )
    return credentials


def get_oauth(scopes=None):
    if scopes is None:
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    # os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"

    creds = None
    token_path = os.path.join(root, 'data/token.pickle')
    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            creds = get_credentials(scopes)
        if not os.path.exists(os.path.dirname(token_path)):
            os.makedirs(os.path.dirname(token_path))
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=creds)

    return youtube


if __name__ == "__main__":
    get_oauth(None)
