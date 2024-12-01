from flask_mysqldb import MySQL

mysql = MySQL()

def init_mysql_db(app):
    mysql.init_app(app)
