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

def retrieveEntries(mp,ds,search,decryptPassword = False):
    db = dbconfig()
    cursor = db.cursor()

    query = ""

    if len(search) == 0:
        query = "SELECT * FROM pm.entries"

    else:
        query = "SELECT * FROM pm.entries WHERE "
        for i in search:
            query += f"{i} = '{search[i]}' AND "
        query = query[:-5]

    cursor.execute(query)
    results = cursor.fetchall()
    if len(results) == 0:
        print("No Results for the search. Sorry")
    if (decryptPassword and len(results)>1) or (not decryptPassword):
        for i in results:
            print(i[0,i[1], i[2], i[3], i[3]])
        return 

    if len(results)==1 and decryptPassword:
        mk = computeMasterKey(mp,ds)
        decrypted = utils.aesutils.decrypt(key=mk, source=results[0][4],keyType="bytes")

        print("Password copied to clipboard")
        pyperclip.copy(decrypted.decode())

    db.close()