import requests
import base64

def getLinkedInUrls():
    print('Getting the linkedInUrls from the website')

    # name application: linkedInProfileParser
    wordpress_user = "linkedInProfileParser"
    wordpress_password = "b9ms H0ZH mmKo WQR5 9Kyu 33PV"
    wordpress_credentials = wordpress_user + ":" + wordpress_password
    wordpress_token = base64.b64encode(wordpress_credentials.encode())
    wordpress_header = {'Authorization': 'Basic ' + wordpress_token.decode('utf-8')}