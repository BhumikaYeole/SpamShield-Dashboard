import pyzmail
from imapclient import IMAPClient

HOST = "imap.gmail.com"
USERNAME = "your_email_address"
PASSWORD = "your_app_password"

def read_latest():
    server = IMAPClient(HOST)
    server.login(USERNAME, PASSWORD)
    server.select_folder('INBOX')

    messages = server.search()

    emails = []

    if len(messages) == 0:
        return None
    else:
        messages = sorted(messages)
        latest_email_id = messages[-20:]

        for id in reversed(latest_email_id):
            raw_message = server.fetch([id], ['BODY[]', 'FLAGS'])
            message = pyzmail.PyzMessage.factory(raw_message[id][b'BODY[]'])

            subject = message.get_subject()
            from_ = message.get_addresses('from')[0][1]

            if message.text_part:         
                body = message.text_part.get_payload().decode(message.text_part.charset)
            else:       
                body = None

            emails.append({
                'subject': subject,
                'from': from_,
                'body': body
            })
        return emails
    

# obj = read_latest()
# print(obj)        
            

        

        