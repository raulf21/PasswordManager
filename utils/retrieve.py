from unittest import result
import utils.aesutils
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
import base64
import pyperclip

from utils.dbconfig import dbconfig

def computeMasterKey(mp,ds):
    password = mp.encode()
    salt = ds.encode()
    key = PBKDF2(password,salt, 32, count= 1000000, hmac_hash_module=SHA512)
    return key

def retrieveEntries(mp,ds,user_id,search,decryptPassword = False):
    if not search or not search.strip():
        print("Invalid search Query")
        return

    try:
        with dbconfig() as db:
            cursor = db.cursor()
            query = "SELECT password FROM pm.entries WHERE website= %s AND user_id= %s"
            val = (search, user_id)
            cursor.execute(query,val)
            result = cursor.fetchone()
    except Exception as e:
        print("Error executing query: ",e)
        db.rollback()
        db.close()
        return

    if not result:
        print("No Results for the search. Sorry")
        return None
    password = result[0]
    if decryptPassword:
        mk = computeMasterKey(mp, ds)
        decrypted = utils.aesutils.decrypt(key=mk, source=password, keyType="bytes")
        return decrypted.decode()

    return None
    