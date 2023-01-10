import argparse
from ctypes import util
from getpass import getpass
from pickle import NONE
from utils.aesutils import decrypt

import utils.newAccount
import utils.retrieve
import utils.passwordgen

import pyperclip
import hashlib
from utils.dbconfig import dbconfig



parser = argparse.ArgumentParser(description='Description')


parser.add_argument('option', help='(a)dd / (r)etrieve /')
parser.add_argument("-s", "--name", help="Site name")
parser.add_argument("-u","--url",help="Site url")
parser.add_argument("-e","--email",help="Email")
parser.add_argument("-l","--login", help="Username")
parser.add_argument("-c","--copy",action='store_true',help='Copy passoword to clipboard.')

args = parser.parse_args()

def inputAndValidateMasterPassword():
    mp = getpass("Master Password: ")
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()

    db = dbconfig()
    cursor = db.cursor()

    query = "SELECT * FROM pm.secret"
    cursor.execute(query)
    result = cursor.fetchall()[0]
    if hashed_mp != result[0]:
        print("WRONG !!")
        return None
    return [mp,result[1]]

def main():
    if args.option in ["add","a"]:
        if args.name == None or args.url == None or args.login == None:
            if args.name == None:
                print("Site Name (-s) required!!")
            if args.url == None:
                print("Site URL (-u) required")
            if args.login == None:
                print("Site Login (-l) required !!!")
            return 

        if args.email == None:
            args.email = ""
        res = inputAndValidateMasterPassword()
        if res is not None:
            utils.newAccount.createEntry(res[0],res[1],args.name, args.url,args.email,args.login)
    if args.option in ["retrieve","r"]:
        res = inputAndValidateMasterPassword()

        search = {}

        if args.name is not None:
            search["website"] = args.name
        if args.url is not None:
            search["siteurl"] = args.url
        if args.email is not None:
            search["email"] = args.email
        if args.login is not None:
            search["username"] = args.login
        if res is not None:
            utils.retrieve.retrieveEntries(res[0],res[1],search,decryptPassword=args.copy)


main()