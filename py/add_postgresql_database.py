import sys

try:
    args = {
        'database_name': sys.argv[1],
        'database_user': sys.argv[2],
        'database_user_password': sys.argv[3]
    }
except IndexError:
    print "DBNAME DBUSER DBUSERPWD"
    exit()

statements = '''
CREATE DATABASE %(database_name)s;
CREATE ROLE %(database_user)s NOCREATEDB LOGIN ENCRYPTED PASSWORD '%(database_user_password)s';
GRANT ALL PRIVILEGES ON DATABASE %(database_name)s TO %(database_user)s;
''' % args

print statements
