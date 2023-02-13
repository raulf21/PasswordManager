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
    db = dbconfig()
    cursor = db.cursor()
    cursor.execute("SELECT password FROM pm.entries WHERE website= %s AND user_id= %s", (search,user_id))
    results = cursor.fetchone()
    db.close()
    if len(results) == 0:
        print("No Results for the search. Sorry")

    if len(results)==1 and decryptPassword:
        mk = computeMasterKey(mp,ds)
        decrypted = utils.aesutils.decrypt(key=mk, source=results[0],keyType="bytes")

        print("Password copied to clipboard")
        pyperclip.copy(decrypted.decode())