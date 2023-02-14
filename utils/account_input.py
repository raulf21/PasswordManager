import re
def take_input():
    response = []

    print("To generate a password for an account please enter the following: ")
    while len(response) < 4:
        website = input("Please Enter Website: ")
        siteurl = input("Please Enter Url: ")
        email = input("Please Enter Email: ")
        username = input("Please Enter Username: ")

        if website and siteurl and email and username:
            if not is_valid_url(siteurl):
                print("Please enter a valid URL.")
                continue
            if not is_valid_email(email):
                print("Please enter a vaild email address.")
            response.append(website)
            response.append(siteurl)
            response.append(email)
            response.append(username)
        else:
            print("All inputs are required. Please provide all inputs.")

    return response
def is_valid_url(url):
    # Define a reular expression pattern for URls
    url_pattern = re.compile(r'^(https?://)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*/?$')
    return url_pattern.match(url) is not None
def is_valid_email(email):
    # Define a regular expression pattern for email addresses
    email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    return email_pattern.match(email) is not None