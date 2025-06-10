import os.path
import pickle 
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sys

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/drive.readonly", "https://www.googleapis.com/auth/calendar.readonly"]


def auth():
    creds = None
    # Uygulamanın PyInstaller ile mi yoksa normal Python ile mi çalıştığını kontrol et
    if getattr(sys, 'frozen', False):
        app_root_path = sys._MEIPASS
    else:
        current_script_dir = os.path.dirname(os.path.abspath(__file__))
        app_root_path = os.path.abspath(os.path.join(current_script_dir, os.pardir))

    token_path = os.path.join(app_root_path, 'token.json')
    credentials_file_path = os.path.join(app_root_path, 'credentials.json')

    if os.path.exists(token_path):
        try:
            with open(token_path, 'rb') as token:
                creds = pickle.load(token)
        except Exception as e:
            print(f"Hata: token.json yüklenirken hata oluştu: {e}. Yeniden kimlik doğrulanacak.")
            creds = None

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file_path, SCOPES) # SCOPES'un tanımlı olduğundan emin olun
            creds = flow.run_local_server(port=0)
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)
    return creds
