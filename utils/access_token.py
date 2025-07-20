from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle, os

class GetAccessToken:
    def __init__(self):
        self.token = None
        self.SCOPES = ['https://mail.google.com/']

    def return_token(self) -> str:
        if os.path.exists('database/token.pickle'):
            with open('database/token.pickle', 'rb') as token:
                self.token = pickle.load(token)
            token.close()
            if self.token and self.token.expired and self.token.refresh_token:
                self.token.refresh(Request())
                with open('database/token.pickle', 'wb') as token:
                    pickle.dump(self.token, token)
                token.close()
            return self.token
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'client_secret/credentials.json', self.SCOPES)
            self.token = flow.run_local_server(port=0)

            with open('database/token.pickle', 'wb') as token:
                pickle.dump(self.token, token)
            token.close()
            return self.token