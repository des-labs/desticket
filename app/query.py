import easyaccess as ea
import sys
import io 
from contextlib import redirect_stdout

def connect_to_db(section='desoper'):
    dbh = ea.connect(section,quiet=True)
    cur= dbh.cursor()
    return (dbh,cur)

def search_username(con,string):
    con[0].do_find_user(string)
    
def query_user(con,email=None,username=None):
    if username:
        query = "SELECT username,email FROM des_users WHERE username='{username}'".format(username=username)
    if email and not username:
        query = "SELECT username,email FROM des_users WHERE email='{email}'".format(email=email)
    con[1].execute(query)
    results=con[1].fetchall()
    return_dict = {'user': results[0][0],'email':results[0][1],'count':len(results)}
    return return_dict

def search(string):
    con = connect_to_db()
    f = io.StringIO()
    with redirect_stdout(f):
        search_username(con,string)
    F = f.getvalue().split('\n')
    return F

def main(username=None, email=None):
    con = connect_to_db()
    results_dict = query_user(con,username=username,email=email)
    return results_dict
