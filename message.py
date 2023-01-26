import os
from oauth2client import client
import base64
from email.message import EmailMessage
from googleapiclient.discovery import build
import requests
import json

# gets credentials to access Gmail API
def getCredentials():
    creds = client.GoogleCredentials(None, 
    os.environ['CLIENT_ID'], 
    os.environ['CLIENT_SECRET'],
    os.environ['REFRESH_TOKEN'],
    None,
    "https://accounts.google.com/o/oauth2/token",
    'thomas')

    return creds

# Call the Gmail API using credentials
def sendMessage(creds):

    service = build('gmail', 'v1', credentials=creds)

    API_KEY = os.environ['API_KEY']

    message = EmailMessage()
    response = requests.get('https://api.wordnik.com/v4/words.json/wordOfTheDay?api_key=' + str(API_KEY))
    message.set_content(str(json.loads(response.text)["word"]) + ' - ' + str(json.loads(response.text)["definitions"][0]['text']))

    message['To'] = '2038325002@txt.att.net'
    message['From'] = 'thomas.s.fenaroli.24@dartmouth.edu'
    message['Subject'] = 'Word of the Day'

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()) \
        .decode()
    create_message = {
        'raw': encoded_message
    }

    send_message = (service.users().messages().send(userId="me", body=create_message).execute())

    return send_message

def lambda_handler(event, context):
    print("running")

    creds = getCredentials()

    send_message = sendMessage(creds)

    print(F'Message Id: {send_message["id"]}')
    
    if send_message:
        return {
            'statusCode': 200,
            'body': json.dumps('Message sent!')
        }
    else:
        return {
            'statusCode': 500,
            'body': json.dumps('Error')
        }