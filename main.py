import newAccount
import updatePassword

def main():
    user_input = ''
    while True:
        user_input = input(
            'Pick one: 1) Add Password, 2) Update Password \n'
        )
        if user_input == '1':
            print('Please prepare account information')
            newAccount.createEntry()
            break
        elif user_input == '2':
            print('Please wait while I create a new Password for you!')
            updatePassword.update()
            break
        else:
            print("Invalid Option")
            continue
main()