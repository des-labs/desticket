import easyaccess as ea

def connect_to_db(section='dessci'):
    dbh = ea.connect(section,quiet=True)
    cur= dbh.cursor()
    return cur


def query_username(username,lastname,firstname,email):
    results = ea.do_find_user(username)

    if len(results) == 1:
        return True
    else:
        return False
