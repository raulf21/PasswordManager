from ctypes import util
from getpass import getpass
import utils.account_input
from utils.aesutils import decrypt
import utils.otp
import utils.accounts
from utils.two_factor import sendemail
import utils.update_password
import utils.breaches

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
        print("3. Update Password")
        print("4. Check for breaches")

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
        elif choice == '3':
            res = inputAndValidateMasterPassword(user_id)
            if res is not None:
                search = input("Please enter the website you need the password updated: ")
                utils.update_password.update(res[0],res[1],user_id,search)
        elif choice == '4':
            res = inputAndValidateMasterPassword(user_id)
            if res is not None:
                unchecked = utils.breaches.get_passwords(user_id)
                breached_websites = utils.breaches.check_all_passwords(unchecked,res[0],res[1])
                if len(breached_websites) > 0:
                    print("The following websites have been breached:")
                    for website in breached_websites:
                        print("-",website)
                        print("Would you like to update these?")
                        change = input("Enter yes or no")
                        if change == 'yes':
                            utils.update_password.update(res[0],res[1],user_id,website[0])
                            print("All breached passwords have been updated.")
                        else:
                            break
                else:
                    print("No breaches have been found.")

main()