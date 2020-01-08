#! /usr/bin/env python

import os
import sys
from jira.client import JIRA
import configparser

class Jira:
    def __init__(self,section):
        parser = configparser.ConfigParser()
        services_path = os.getenv('DES_SERVICES')
        if not services_path:
            services_path = os.path.join(os.getenv('HOME'),'.desservices.ini')
        with open(services_path) as configfile:
            parser.read_file(configfile)
        jiradict=parser[section]
        jirauser=jiradict['user']
        jirapasswd=jiradict['passwd']
        jiraserver=jiradict['server']
        jira=JIRA(options={'server':jiraserver},basic_auth=(jirauser,jirapasswd))
        self.jira = jira
        self.server = jiraserver
        self.user = jirauser

    def search_for_issue(self,email):
        jql = 'summary ~ "Help with DESDM account" \
               and project = "DESHELP" \
               and text ~ "Reset my passwords" \
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

    def add_jira_comment(self,issue,comment):
        self.jira.add_comment(issue,comment)
