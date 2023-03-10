from cgi import test
from ctypes import util
import utils.passwordgen as passwordgen
import base64
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import utils.aesutils
from utils.dbconfig import dbconfig

def computeMasterKey(mp,ds):
    password = mp.encode()
    salt = ds.encode()
    key = PBKDF2(password,salt, 32, count= 1000000, hmac_hash_module=SHA512)
    return key

def createEntry(mp,ds,user_id,sitename, url, email,username):
    try:
        password  = passwordgen.createPassword()
        mk = computeMasterKey(mp,ds)

        encrypted = utils.aesutils.encrypt(key=mk,source=password,keyType="bytes")
        with dbconfig() as db, db.cursor() as cursor:
            query = "INSERT INTO pm.entries (user_id,website,siteurl,email,username, password) values (%s,%s,%s,%s,%s,%s)"
            val = (user_id,sitename, url, email, username, encrypted)
            cursor.execute(query,val)
            db.commit()
    except Exception as e:
        print(f"Error occured during database transaction or encryption: {e}")
        db.rollback()
        db.close()
    finally:
        db.close()
    print("Added Entry")
