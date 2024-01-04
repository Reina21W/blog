SECRET_KEY = "aedcfver"

HOSTNAME = "127.0.0.1"
PORT = '3306'
USERNAME = "root"
PASSWORD = "0221"
DATABASE = "coursework"

DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
