from jira.client import JIRA
import base64
import yaml
import smtplib
import datetime
from html.parser import HTMLParser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr

#Usage: resolve ticket username --reset
# username is DB username
# if --reset then do unlock and reset and send email accordingly
#
# read from arguments jira ticket
# extract name and Email
# assign ticket
# unlock and reset user depending options 1/2
# send email depending of option 1/2
# close ticket

#templates


def send_email():
    msg = MIMEMultipart()
    fromemail = 'audreyk@illinois.edu'
    toemail = 'audrey@koziol.cc'
    server = 'smtp.ncsa.illinois.edu'
    s = smtplib.SMTP(server)
    msg['Subject'] = 'DESDM Account'
    msg['From'] = formataddr((str(Header('DESDM Release Team', 'utf-8')), fromemail))
    msg['To'] = fromemail
    with open("emailbody.html") as file: 
        file_contents = file.read()
    name = "Audrey"
    password = "user password"
    date = datetime.datetime.now()
    email_body = file_contents.format(Username=name, password = password, date = date)    
    #body = "Password was reset to <b> test</b> <br> Thanks "
    #msg.attach(MIMEText(body, 'html'))
    s.sendmail(fromemail, toemail, email_body)
    s.quit()


with open('access.yaml', 'r') as cfile:
    conf = yaml.load(cfile)['jira']
u = base64.b64decode(conf['uu']).decode().strip()
p = base64.b64decode(conf['pp']).decode().strip()
jira = JIRA(server='https://opensource.ncsa.illinois.edu/jira/',
            basic_auth=(u, p))
j = jira.search_issues('key=DESHELP-331')[0]
body = j.fields.description
for line in body.split('\n'):
    if line.startswith('Email'):
        line = ''.join(line.split())
        email = line[line.index(':') + 1:]
        print(email)
    if line.startswith('Name'):
        name = line.split('Name : ')[-1]
        print(name)

send_email()

#jira.assign_issue(j, 'desdm-wufoo')
#jira.add_comment(j, 'email sent')
#jira.transition_issue(j, '2')
