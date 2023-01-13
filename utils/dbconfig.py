import mysql.connector

def dbconfig():
    try:
        db = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            passwd = ''#password to your mysql
        )
        return db
    except Exception as e:
        print(str(e))

