import psycopg2
import passwordgen
def createEntry():
    try:
        connection = psycopg2.connect(database='postgres',
                                host='localhost',
                                user='postgres',
                                password='',
                                port='5432')
        postgres_insert_query = """INSERT INTO accounts(website,username, pass) VALUES (%s,%s,%s) """

        cursor = connection.cursor() 

        website = input('Please enter the website: ')
        username = input('Please enter the username: ')
        password  = passwordgen.createPassword()

        record_to_insert = (str(website),str(username),str(password))
        cursor.execute(postgres_insert_query,record_to_insert)
        connection.commit()
        count = cursor.rowcount
        print(count, "RECORD inserted successfully")
    except (Exception, psycopg2.Error) as error:
        print('Failed to insert credientials for account!')
    finally:
        if connection:
            cursor.close()
            connection.close()
            print('PostgreSQL connection is closed')