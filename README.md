# PasswordManager
This project provides a set of functions for storing and retrieving password entries in a database, as well as for encrypting and decrypting the passwords. The code uses the AES encryption algorithm, the PBKDF2 key derivation function, and the SHA-512 hash function. The project also includes a password generator, which creates a random password for the user. The code also includes a command-line interface for adding and retrieving password entries from the database.

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

``` python main.py -h
usage: main.py [-h] [-s NAME] [-u URL] [-e EMAIL] [-l LOGIN] [-c] option
Description:
positional arguments:
  option                (a)dd / (r)etrieve /

options:
  -h, --help            show this help message and exit
  -s NAME, --name NAME  Website name
  -u URL, --url URL     website url
  -e EMAIL, --email EMAIL
                        Email
  -l LOGIN, --login LOGIN
                        Username
  -c, --copy            Copy passoword to clipboard. 
  ```
  
Adding Entries:

``` python main.py add -s "website_name" -u "url_name" -e "email_enough" -l "username"```

Getting passwords:


```python main.py retireve -s "website_name"```


Note:substitute "-s" for any other of the options above.

### Notes
Make sure that the dependencies are installed and the dbconfig.py file is properly configured with the database connection details before running the code.
Handle the Master Password and Salt in a secure way.
You can run the code by using the command ```python main.py -h``` for getting help on how to run the code

Future Work
Add more features such as editing entries.
GUI implementation.
Add more encryption options.
