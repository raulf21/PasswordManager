# PasswordManager
This project provides a set of functions for storing and retrieving password entries in a database, as well as for encrypting and decrypting the passwords. The code uses the AES encryption algorithm, the SHA-256 hash function, and the pyperclip library for copying the password to the clipboard. The project also includes a password generator, a command-line interface for adding and retrieving password entries from the database and two-factor authentication.

### Dependencies
* pycryptodome library

* pyperclip library

### Installations:

```pip install -r requirements.txt```


### Database setup:
* Login as root user:

    ```mysql -u root -p```

* Create user:

    ```CREATE USER 'pm'@localhost IDENTIFIED BY 'password';```

* Granting Privilages:

    ```GRANT ALL PRIVILEGES ON *.* TO 'pm'@localhost;```

### Run

You first need need to configure the password manager by creating a MASTER password. Only needs to be done once.

```python config.py```



### Usage

 
When running the main.py file, you will be prompted to either sign in or create an account. 
```
1. Sign In
2. Create an Account
```
Sign in:
```
Email:
Password:
```
Create an Account:
```
Email: 
Password: 
To finish creating your account we need a password only you will remember.
Choose a MASTER PASSWORD: 
Re-type:
```

Once you have signed in or created an account, you will have the option to:

```
1. Add an Account
2. Retrieve Password
3. Update Password
4. Check for breaches
```

When adding an account, you will be prompted to enter:
```
website name:
website URL:
email:
username:
```
Password is generated for you automatically.

When retrieving a password, you will be prompted to enter the website name. 
Password will be copied to clipboard.

When updating a password, you will be prompted to enter:
```
Master Password:
website: 
```
Password will be generated automatically.

Checking for Breaches:
```
Enter Master Password:
```
If password has been breached:
```
Would you like to update these?
Enter yes or no?
```
Selecting yes will update them automatically for you.

  

### Notes
Make sure that the dependencies are installed and the dbconfig.py file is properly configured with the database connection details before running the code.
Handle the Master Password and Salt in a secure way.

### Future Work
* Implement a GUI for the project to make it more user-friendly.
* Add a feature for password recovery in case the user forgets their master password.

