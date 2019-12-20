import easyaccess as ea

def connect_to_db(section='desoper'):
    dbh = ea.connect(section,quiet=True)
    cur= dbh.cursor()
    return cur


def query_username(con,username):
    #results = con.do_find_user(username)
    query = "SELECT count(*) FROM des_users WHERE username='{username}'".format(username=username)
    con.execute(query)
    results=con.fetchall()[0][0]
    if results == 1:
        return True
    else:
        return False

def main(username):
    con = connect_to_db()
    is_user = query_username(con,username)
    return is_user
