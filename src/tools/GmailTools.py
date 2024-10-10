import os, re
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
import base64
from datetime import datetime, timedelta

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailToolsClass:
    def __init__(self):
        self.service = self._get_gmail_service()

    def fetch_recent_emails(self, max_results=50):
        try:
            one_day_ago = (datetime.now() - timedelta(days=1)).strftime('%Y/%m/%d')
            query = f'after:{one_day_ago} to:me'
            results = self.service.users().messages().list(userId="me", q=query, maxResults=max_results).execute()
            messages = results.get('messages', [])
            
            email_list = []
            for message in messages:
                email_info = self._get_email_info("me", message['id'])
                if email_info:  # Only append if email_info is not None
                    email_list.append(email_info)
            
            return email_list
        
        except Exception as error:
            print(f"An error occurred while fetching emails: {error}")
            return []

    def create_draft_reply(self, id, sender, subject, reply_text, user_id='me'):
        try:
            message = self._create_reply_message(sender, subject, reply_text, id)
            draft = self.service.users().drafts().create(userId=user_id, body={
                'message': {
                    'raw': self._encode_message(message)
                }
            }).execute()
            print(f"Draft created for email from {sender} with subject '{subject}'")
            return draft
        except Exception as error:
            print(f"An error occurred while creating draft: {error}")
            return None
        
    def send_reply(self, id, sender, subject, reply_text, user_id='me'):
        try:
            message = self._create_reply_message(sender, subject, reply_text, id)
            sent_message = self.service.users().messages().send(userId=user_id, body={
                'raw': self._encode_message(message)
            }).execute()
            print(f"Reply sent to {sender} with subject '{subject}'")
            return sent_message
        except Exception as error:
            print(f"An error occurred while sending reply: {error}")
            return None
        
    def _get_gmail_service(self):
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        
        return build('gmail', 'v1', credentials=creds)

    def _get_email_info(self, user_id, msg_id):
        msg = self.service.users().messages().get(userId=user_id, id=msg_id, format='full').execute()
        headers = msg['payload']['headers']
        sender = next((header['value'] for header in headers if header['name'].lower() == 'from'), 'Unknown')
        sender = re.search(r'<(.*?)>', sender).group(1) if re.search(r'<(.*?)>', sender) else None
        subject = next((header['value'] for header in headers if header['name'].lower() == 'subject'), 'No Subject')
        body = self._get_email_body(msg)
        body = self._clean_body_text(body)
        return {
            'id': msg_id,
            'sender': sender,
            'subject': subject,
            'body': body
        }

    def _get_email_body(self, msg):
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['mimeType'] == 'text/plain':
                    return base64.urlsafe_b64decode(part['body']['data']).decode('utf-8')
        elif 'body' in msg['payload']:
            return base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')
        return ''
    
    def _clean_body_text(self, text):
        # Remove carriage returns and newlines
        cleaned_text = text.replace('\r', '').replace('\n', '')
        
        # Replace multiple spaces with a single space
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
        
        # Remove leading and trailing whitespace
        cleaned_text = cleaned_text.strip()
        
        return cleaned_text

    def _create_reply_message(self, sender, subject, reply_text, original_msg_id):
        message = MIMEText(reply_text)
        message['to'] = sender
        message['subject'] = f"Re: {subject}"
        message['In-Reply-To'] = original_msg_id
        message['References'] = original_msg_id
        return message

    def _encode_message(self, message):
        return base64.urlsafe_b64encode(message.as_bytes()).decode()