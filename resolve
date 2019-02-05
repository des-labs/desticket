#!/usr/bin/env python3
from jira.client import JIRA
import base64
import yaml
import smtplib
import datetime
import easyaccess as ea
import io
import contextlib
from html.parser import HTMLParser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr
import argparse


def unlock(user, db, reset=True):
    print('[ ... ] Reseting password in {} ...'.format(db))
    con = ea.connect(db)
    done = False
    if reset:
        cmd = "unlockuser({},'reset')".format(user)
    else:
        cmd = "unlockuser({})".format(user)
    temp = io.StringIO()
    with contextlib.redirect_stdout(temp):
        con.do_execproc(cmd)
    out = temp.getvalue()
    if 'Done' in out:
        done = True
    return done, out


def send_email(name, username, email, reset):
    msg = MIMEMultipart('alternative')
    fromemail = 'mcarras2@illinois.edu'
    toemail = email
    server = 'smtp.ncsa.illinois.edu'
    s = smtplib.SMTP(server)
    msg['Subject'] = 'DESDM Account'
    msg['From'] = formataddr((str(Header('DESDM Release Team', 'utf-8')), fromemail))
    msg['To'] = toemail
    if reset:
        with open("templates/reset.html") as file:
            file_contents = file.read()
    else:
        with open("templates/unlock.html") as file:
            file_contents = file.read()
    email_body = file_contents.format(name=name, user=username, user2=username[0:3])
    msg.attach(MIMEText(email_body, 'html'))
    print('[ ... ] Emailing {} at {}'.format(name, toemail))
    s.sendmail(fromemail, toemail, msg.as_string())
    s.quit()
    # with open('test.html', 'w') as test:
    #    test.write(email_body)
    # return email_body


def read_ticket(ticket):
    print('[ ... ] Gathering information from DESHELP-{}'.format(ticket))
    with open('access.yaml', 'r') as cfile:
        conf = yaml.load(cfile)['jira']
    u = base64.b64decode(conf['uu']).decode().strip()
    p = base64.b64decode(conf['pp']).decode().strip()
    jira = JIRA(server='https://opensource.ncsa.illinois.edu/jira/',
                basic_auth=(u, p))
    j = jira.search_issues('key=DESHELP-{}'.format(ticket))[0]
    body = j.fields.description
    for line in body.split('\n'):
        if line.startswith('Email'):
            line = ''.join(line.split())
            email = line[line.index(':') + 1:]
        if line.startswith('Name'):
            name = line.split('Name : ')[-1]
    return name, email


def resolve_ticket(ticket):
    print('[ ... ] Closing DESHELP-{}'.format(ticket))
    with open('access.yaml', 'r') as cfile:
        conf = yaml.load(cfile)['jira']
    u = base64.b64decode(conf['uu']).decode().strip()
    p = base64.b64decode(conf['pp']).decode().strip()
    jira = JIRA(server='https://opensource.ncsa.illinois.edu/jira/',
                basic_auth=(u, p))
    j = jira.search_issues('key=DESHELP-{}'.format(ticket))[0]
    try:
        jira.assign_issue(j, 'desdm-wufoo')
        jira.add_comment(j, 'email sent')
        jira.transition_issue(j, '2')
    except:
        pass


def run_all(ticket, user, reset=True):
    name, email = read_ticket(ticket)
    check, msg = unlock(user, 'dessci', reset)
    if not check:
        print('dessci')
        print(msg)
        print('** ERROR **')
        return
    check, msg = unlock(user, 'desoper', reset)
    if not check:
        print('desoper')
        print(msg)
        print('** ERROR **')
        return
    send_email(name, user, email, reset)
    resolve_ticket(ticket)
    print('[ ... ] All Done!')


def run_manual(user, reset=True, email='', name=''):
    check, msg = unlock(user, 'dessci', reset)
    if not check:
        print('dessci')
        print(msg)
        print('** ERROR **')
        return
    check, msg = unlock(user, 'desoper', reset)
    if not check:
        print('desoper')
        print(msg)
        print('** ERROR **')
        return
    send_email(name, user, email, reset)
    print('[ ... ] All Done!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Resolve ticket, for manually entered ticket use 0')
    parser.add_argument('ticket', help="Just the ticket number from JIRA DESHELP-NNN, e.g.: 333, use 0 for manual entry")
    parser.add_argument('username', help="DB username")
    parser.add_argument('--just_unlock', '-ju', help="just unlock but do not reset password")
    parser.add_argument('--email', help="manually entered email")
    parser.add_argument('--name', help="manually entered name")
    args = parser.parse_args()
    ticket = args.ticket
    username = args.username
    reset = not args.just_unlock
    action = 'Unlock and reset' if reset else 'Just unlock'
    print()
    print('[ ... ] {} password for {}. Ticket DESHELP-{} ...'.format(action, username, ticket))
    print()
    if int(ticket) == 0:
        run_manual(username, reset, email = args.email, name = args.name)
    else:
        run_all(ticket, username, reset)
