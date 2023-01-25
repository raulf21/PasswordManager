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
    password  = passwordgen.createPassword()
    mk = computeMasterKey(mp,ds)

    encrypted = utils.aesutils.encrypt(key=mk,source=password,keyType="bytes")

    db = dbconfig()

    cursor = db.cursor()
    query = "INSERT INTO pm.entries (user_id,website,siteurl,email,username, password) values (%s,%s,%s,%s,%s,%s)"
    val = (user_id,sitename, url, email, username, encrypted)
    cursor.execute(query,val)
    db.commit()
    db.close()

    print("Added Entry")
