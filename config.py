from getpass import getpass
import os
import sys
import hashlib
import random
import string
from utils.dbconfig import dbconfig

def generateDeviceSecret(length=10):
    return ''.join(random.choices(string.ascii_uppercase+string.digits,k=length))


def config():
    db = dbconfig()
    cursor = db.cursor()

    try:
        cursor.execute("CREATE DATABASE pm")
    except Exception as e:
        print('An error has occured while trying to create db.')
        print(str(e))
        sys.exit(0)
    print("Database 'pm' created")

    # Create tables
    users_table = """CREATE TABLE pm.users(
        id INT(11) AUTO_INCREMENT PRIMARY KEY,
        email VARCHAR(255) NOT NULL unique,
        password_hash VARCHAR(255) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
    cursor.execute(users_table)

    secrets_table = """CREATE TABLE pm.secret (
        id INT(11) AUTO_INCREMENT PRIMARY KEY,
        user_id INT(11) NOT NULL,
        masterkey_hash VARCHAR(256) NOT NULL, 
        device_secret TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES pm.users(id) ON DELETE CASCADE
        );
        """
    cursor.execute(secrets_table)
    print("Table 'secrets' created")


    otps_table = """CREATE TABLE pm.otp (
        id INT(11) AUTO_INCREMENT PRIMARY KEY,
        user_id INT(11) NOT NULL,
        otp TEXT NOT NULL, 
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expiration TIMESTAMP NOT NULL, 
        used TINYINT(1) DEFAULT 0,
        secret VARCHAR(255),
        FOREIGN KEY (user_id) REFERENCES pm.users(id) ON DELETE CASCADE
        );
        """
    cursor.execute(otps_table)
    print("Table 'OTPS' created")

    entries_table = """CREATE TABLE pm.entries (
        id INT(11) AUTO_INCREMENT PRIMARY KEY,
        user_id INT(11) NOT NULL,
        website VARCHAR(255) NOT NULL,
        siteurl VARCHAR(255) NOT NULL, 
        email VARCHAR(255) NOT NULL, 
        username VARCHAR(255) NOT NULL, 
        password VARCHAR(255) NOT NULL,
        FOREIGN KEY (user_id) REFERENCES pm.users(id) ON DELETE CASCADE
        );
        """
    cursor.execute(entries_table)
    print("Table 'entries' created")

    db.commit()

    print("Added to database")
    print("Configuration done")

    db.close()


config()


    