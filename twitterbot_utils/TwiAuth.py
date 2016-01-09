import tweepy, webbrowser, os

class TwiAuth():
    def __init__(self):
        self.consumer_key = os.environ.get('consumer_key')
        self.consumer_secret = os.environ.get('consumer_secret')
        self.auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)

    def do_auth(self):
        webbrowser.open(self.auth.get_authorization_url())
        verifier = raw_input('PIN: ').strip()
        self.auth.get_access_token(verifier)
        print u'export user_access_token=' + self.auth.access_token
        print u'export user_access_secret=' + self.auth.access_token_secret

if __name__ == '__main__':
    TwiAuth().do_auth()
