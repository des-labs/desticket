#! /usr/bin/env python

import os
import sys
from jira.client import JIRA
import configparser
import yaml
import base64
from app import app

class Jira:
    def __init__(self):
        with open(app.config['ACCESS_PATH'], 'r') as cfile:
            conf = yaml.load(cfile)['jira']
        u = base64.b64decode(conf['uu']).decode().strip()
        p = base64.b64decode(conf['pp']).decode().strip()
        jira=JIRA(options={'server': 'https://opensource.ncsa.illinois.edu/jira'},basic_auth=(u,p))
        self.jira = jira

    def search_for_issue(self,email):
        jql = 'summary ~ "Help with DESDM account" \
               and project = "DESHELP" \
               and (text ~ "Reset my passwords" | text ~ "Forgot DB credentials") \
               and status = "Open" \
               and text ~ "Email: {email}"'.format(email=email)
        issue = self.jira.search_issues(jql)
        return issue
 
    def create_jira_ticket(self,project,summary,description,assignee):
        ticket_dict = {'project':{'key':project},
		    'summary': summary,
		    'issuetype':{'name':'Processing Request'},
		    'description': description,
		    'assignee':{'name': assignee},
		    }	
        ticket = self.jira.create_issue(fields=ticket_dict)
        return ticket.key	

