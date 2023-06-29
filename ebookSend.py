import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

import pandas as pd
import json

# Load the data
df = pd.read_excel('Order_checked.xlsx')

# Filter by the 'check' column
df = df[df['check'] == 'O']

# Set email details
my_email = 'jisoolee031@gmail.com'
subject = 'Here is your Ebook'

# Prepare the ebook
filename = 'Ebook.pdf'
attachment = open(filename, 'rb')
body = 'Find the Ebook attached.'

# Load the account configuration
with open('AccountConfig.json') as json_file:
    data = json.load(json_file)
app_password = data['app_password']

# Send the email to each recipient
for recipient in df['Email']:
    msg = MIMEMultipart()
    msg['From'] = my_email
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename= {filename}')

    msg.attach(part)

    text = msg.as_string()

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(my_email, app_password)
        server.sendmail(my_email, recipient, text)

attachment.close()
