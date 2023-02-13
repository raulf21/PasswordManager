import utils.aesutils
import utils.passwordgen as passwordgen

from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from utils.dbconfig import dbconfig

def computeMasterKey(mp,ds):
    password = mp.encode()
    salt = ds.encode()
    key = PBKDF2(password,salt, 32, count= 1000000, hmac_hash_module=SHA512)
    return key

def update(mp,ds,user_id,search):
    mk = computeMasterKey(mp,ds)

    new_password = passwordgen.createPassword()
    print(new_password)
    encrypted = utils.aesutils.encrypt(key=mk,source=new_password,keyType="bytes")
    db = dbconfig()
    cursor = db.cursor()
    query = "UPDATE pm.entries SET password = %s WHERE website= %s AND user_id= %s"
    cursor.execute(query,(encrypted,search,user_id))
    db.commit()
    print("Password updated")
    db.close()

    