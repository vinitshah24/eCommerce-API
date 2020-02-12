# MYSQL
mysql_db_username = 'root'
mysql_db_password = 'root'
mysql_db_hostname = 'localhost'
mysql_db_name = 'flask_rest_db'

DEBUG = True
PORT = 5000
HOST = "127.0.0.1"
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = "MERKY"

SQLALCHEMY_DATABASE_URI = "mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_ADDR}/{DB_NAME}" \
    .format(DB_USER=mysql_db_username,
            DB_PASS=mysql_db_password,
            DB_ADDR=mysql_db_hostname,
            DB_NAME=mysql_db_name)
