from ctypes import util
from getpass import getpass
import utils.account_input
from utils.aesutils import decrypt
import utils.otp
import utils.accounts
from utils.two_factor import sendemail

import utils.newAccount
import utils.retrieve
import utils.passwordgen

import pyperclip
import hashlib

from utils.dbconfig import dbconfig


def inputAndValidateMasterPassword(user_id):
    mp = getpass("Master Password: ")
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()

    db = dbconfig()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM pm.secret WHERE id= %s", (user_id,))
    result = cursor.fetchone()
    if hashed_mp != result[2]:
        print("WRONG !!")
        return None
    return [mp,result[3]]

def main():
    print("1. Sign in.")
    print("2. Create an account.")

    choice = input("Please enter your choice.")

    if choice == '1':
        user_id = utils.accounts.sign_in()
    elif choice == '2':
        user_id = utils.accounts.signup()
    else:
        print("Invalid Option")
    while user_id:
        print("What would you like to do?")
        print("1. Add an account")
        print("2. Retrieve Password: ")

        choice = input("Please enter your choice. ")
        if choice == '1':
            res = inputAndValidateMasterPassword(user_id)
            if res is not None:
                response = utils.account_input.take_input()
                utils.newAccount.createEntry(res[0],res[1],user_id,response[0], response[1],response[1],response[2])
        elif choice == '2':
            res = inputAndValidateMasterPassword(user_id)
            if res is not None:
                search = input("Please enter the website you need the password for: ")
                utils.retrieve.retrieveEntries(res[0],res[1],user_id,search,decryptPassword =True)
                
main()