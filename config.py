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
    query = "CREATE TABLE pm.secret (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
    res = cursor.execute(query)
    print("Table 'secrets' created")

    query = "CREATE TABLE pm.entries (website TEXT NOT NULL,siteurl TEXT NOT NULL, email TEXT, username TEXT, password TEXT NOT NULL)"
    res = cursor.execute(query)
    print("Table 'entries' created")

    while 1:
        master = getpass("Choose a MASTER PASSWORD: ")
        if master ==getpass("Re-type: ") and master !="":
            break
        print("Please Try Again.")
    #hash the Master Password

    hashed_mp = hashlib.sha256(master.encode()).hexdigest()
    print("Generated hash of Master Program")

    #Geneter a Device Secret
    ds = generateDeviceSecret()
    print("Device Secret generated")

    #Add them to db
    query="INSERT INTO pm.secret (masterkey_hash,device_secret) values (%s,%s)"
    val = (hashed_mp, ds)
    cursor.execute(query,val)
    db.commit()

    print("Added to database")
    print("Configuration done")

    db.close()


config()


    