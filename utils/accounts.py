from utils.dbconfig import dbconfig
import bcrypt
import os
import sys
import hashlib
import random
import string
from getpass import getpass


"""
bycrypt: - uses a unique salt for each password hash,
so even if two users have the same password, their
hashed passwords will be different. This will make it more
difficult for an attacker to use precomputed tables of common passwords
to crack the hash.
"""
def generateDeviceSecret(length=10):
    return ''.join(random.choices(string.ascii_uppercase+string.digits,k=length))
def sign_in():
    email = input("Email: ")
    password = getpass("Password: ")
    
    db = dbconfig()
    cursor = db.cursor()

    # Retrieve the user's hashed password from the database
    cursor.execute("SELECT id, password_hash FROM pm.users WHERE email = %s", (email,))

    result = cursor.fetchone()

    # If the email exists in the database
    if result:
        # Compare the input password with the hashed password in the database
        # checkpw() function is used to verify the password provided against the hashed password
        if bcrypt.checkpw(password.encode('utf-8'),result[1].encode('utf-8')):
            print("Welcome back, {}!".format(email))
            return result[0]
        else:
            print("Incorrect password.")
    else:
        print("This email is not registered.")
    db.close()

def signup():
    email = input("Email: ")
    password = getpass("Password: ").encode()

    # Hash the password using bcrypt
    '''gensalt() - generates a new random salt
                 - also accepts a 'log_rounds' parameter, 
                 which controls the number of hashing round 
                 and thus the computational effort required 
                 to hash the password
                 - the default is 12 rounds but you can increase
                  this number for added security
       hashpw()-combines the password and salt   
    '''
    hashed_password = bcrypt.hashpw(password,bcrypt.gensalt())
    db = dbconfig()
    cursor = db.cursor()

    # Insert the new user into the database
    cursor.execute("INSERT INTO pm.users (email,password_hash) VALUES (%s,%s)",(email,hashed_password))

    cursor.execute("SELECT id FROM pm.users WHERE email= %s", (email,))
    result = cursor.fetchone()

    print("To finish creating your account we need a password only you will remember.")
    while 1:
        master = getpass("Choose a MASTER PASSWORD: ")
        if master == getpass("Re-type: ") and master !="":
            break
        print("Please Try Again.")

    #hash the Master Password
    hashed_mp = hashlib.sha256(master.encode()).hexdigest()
    print("Generated hash of Master Program")

    #Generate a Device Secret
    ds = generateDeviceSecret()
    print("Device Secret generated")

    #Add them to db
    query="INSERT INTO pm.secret (user_id,masterkey_hash,device_secret) values (%s,%s,%s)"
    val = (result[0],hashed_mp, ds)
    cursor.execute(query,val)

    db.commit()
    print("Account created!")
    db.close()
    return result[0]