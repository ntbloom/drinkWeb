#! usr/bin python3

#funBook.py - gives you something fun to read in your spare time

import requests
# requests module is 3rd party, install using PIP
import argparse
import random
import codecs

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


parser = argparse.ArgumentParser()
parser.add_argument("--printing", type=bool, default=True, help="Whether or not to print to the console.")
parser.add_argument("--sender_email", type=str, default="alltoolsintheshadowofthemoon@gmail.com", help="sender email.")
parser.add_argument("--sender_pw", type=str, default="M0byd!ck", help="sender password.")
parser.add_argument("-r", "--rec_file", type=str, default="funBook_recipients.txt", help="txt file with one recipient email per line.")

args = parser.parse_args()

# connect to the book
book = requests.get('http://www.gutenberg.org/cache/epub/2489/pg2489.txt')
book.raise_for_status()

# loop through and count paragraphs at are longer than a single line
i = 0
candidates = []
for chunk in book.iter_content(100000):
    text = codecs.decode(chunk, 'unicode_escape') # decode the weirdly coded text characters (like \\n for newline and \\r for paragraph, etc.)
    paragraphs = text.split("\n\r\n") # split on paragraph seperator
    for p in paragraphs:
        i = i + 1 # increment paragraph counter
        if '\n' in p: # if it's more than a single line, like a chapter heading
            candidates += [i]

# pick a random paragraph number
pick = random.choice(candidates)

# loop back through and get that paragraph's text
i = 0
for chunk in book.iter_content(100000):
    text = codecs.decode(chunk, 'unicode_escape') # decode the weirdly coded text characters (like \\n for newline and \\r for paragraph, etc.)
    paragraphs = text.split("\n\r\n") # split on paragraph seperator
    for p in paragraphs:
        i = i + 1 # increment paragraph counter
        if i == pick: # if it's more than a single line, like a chapter heading
            title = 'paragraph {}'.format(i)
            p_text = p.replace('\n', ' ').replace('\r', '')
            if args.printing:
                print(title + '\n' + p_text)

# build email
msg = MIMEMultipart()
msg['From'] = args.sender_email
msg['Subject'] = title
msg.attach(MIMEText(p_text, 'plain'))

# convert message for sending
text = msg.as_string()

# set up email server connection
server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server.login(args.sender_email, args.sender_pw)

# get recipients from file
with open(args.rec_file, 'r') as f:
    recipients = f.read().split('\n')

# filter out any invalid emails (or blank lines)
recipients = [rec for rec in recipients if '@' in rec]

# send emails
for rec in recipients:
    server.sendmail(args.sender_email, rec, text)

server.quit()
