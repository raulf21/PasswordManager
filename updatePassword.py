import psycopg2
import passwordgen
def update():
    try:
        connection = psycopg2.connect(database='postgres',
                                host='localhost',
                                user='postgres',
                                password='',
                                port='5432')
        cursor = connection.cursor() 

        sql_select_query = """SELECT * FROM accounts where website = %s"""

        website = input('Please enter the website: ')
        password  = passwordgen.createPassword()

        cursor.execute(sql_select_query,(website,))
        record = cursor.fetchone()
        print(record)

        sql_update_query = """UPDATE accounts set pass = %s where website = %s"""
        cursor.execute(sql_update_query,(password, website))

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