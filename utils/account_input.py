def take_input():
    response = []

    print("To generate a password for an account please enter the following: ")
    while len(response) < 4:
        website = input("Please Enter Website: ")
        siteurl = input("Please Enter Url: ")
        email = input("Please Enter Email: ")
        username = input("Please Enter Username: ")

        if website and siteurl and email and username:
            response.append(website)
            response.append(siteurl)
            response.append(email)
            response.append(username)
        else:
            print("All inputs are required. Please provide all inputs.")

    return response
