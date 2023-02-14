from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA512
from Crypto.Random import get_random_bytes
from utils.dbconfig import dbconfig
import requests
import utils.aesutils
import hashlib
def computeMasterKey(mp,ds):
    password = mp.encode()
    salt = ds.encode()
    key = PBKDF2(password,salt, 32, count= 1000000, hmac_hash_module=SHA512)
    return key

def get_passwords(user_id):
    db = dbconfig()
    cursor = db.cursor()

    query = "SELECT website,password FROM pm.entries WHERE user_id = %s"
    cursor.execute(query,(user_id,))

    result = cursor.fetchall()
    passwords = [(row[0],row[1]) for row in result]

    return passwords




def check_password_breach(password,mk):
    """
    Parameters:
    password = the encrypted password from the database
    master_key - the key used to encrypt the password

    return Boolean indicating if the password has been breached or not
    """
    decrypted_password = utils.aesutils.decrypt(key=mk,source=password,keyType="bytes")
    decrypted_password = decrypted_password.decode()
    sha1 = hashlib.sha1(decrypted_password.encode()).hexdigest().upper()
    response = requests.get(f'https://api.pwnedpasswords.com/range/{sha1[:5]}')

    if sha1[5:].upper() in response.text:
        return True
    return False
def check_all_passwords(passwords,mp,ds):
    """
    Parameters:
    passwords - a list of encrypted passwords from the database
    master_key - a key used to encrypt the passwords

    return a list of tuples containing the encrypted password and a boolean indicating if it has been breached
    """
    mk = computeMasterKey(mp,ds)
    results = []
    for website,password in passwords:
        breached = check_password_breach(password,mk)
        if breached == True:
            results.append((website,password,breached))
    return results