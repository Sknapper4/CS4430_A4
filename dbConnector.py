import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode


# from main import menu

def get_db_connection():
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='northwind',
                                             user='root',
                                             password='Sknapper4.0')
        return connection
    except mysql.connector.Error as error:
        print('Failed to connnect to database {}'.format(error))
    # menu()


def close_db_connection(connection):
    try:
        connection.close()
    except mysql.connector.Error as error:
        print('Failed to close database connection {}'.format(error))


def read_db_version():
    try:
        connection = get_db_connection()
        db_info = connection.get_server_info()
        print('Connected to MySQL database. MySQL Server version is ', db_info)
        cursor = connection.cursor()
        cursor.execute('Select database();')
        record = cursor.fetchone()
        print('You\'re connected to -', record)
        close_db_connection(connection)
    except mysql.connector.Error as error:
        print('Failed to read database version {}'.format(error))
    # menu()


def read_from_db():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql_query = 'select * from %s' % 'products'

        cursor.execute(sql_query)
        records = cursor.fetchall()

        print('Records')
        for row in records:
            print(row)

        close_db_connection(connection)
    except mysql.connector.Error as error:
        print('Failed '.format(error))
    # menu()


def add_customer():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        add_value_string = get_customer_tbl_vals()
        sql_query = f'INSERT INTO customers VALUES {add_value_string}'
        cursor.execute(sql_query)
        sql_query = 'SELECT * FROM customers'
        cursor.execute(sql_query)
        records = cursor.fetchall()
        for row in records:
            print(row)
    except mysql.connector.Error as error:
        print('Failed {}'.format(error))
    # menu()


def get_customer_tbl_vals():
    customer_id = input('Please enter the customer ID')
    check_customer_existence(customer_id)
    company_name = input('Please enter company name')
    contact_name = input('Please enter the contacts name')
    contact_title = input('Please enter the contacts title')
    address = input('Please enter the address')
    city = input('Please enter the city')
    region = input('Please enter the region')
    postal_code = input('Please enter the postal code')
    country = input('Please enter the country')
    phone = input('Please enter the phone number')
    fax = input('Please enter the fax number')

    return f'({customer_id}, {company_name},{contact_name},{contact_title},{address}, {city}, {region}, {postal_code},{country}, {phone}, {fax})'


def check_customer_existence(customer_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql_query = f'SELECT CustomerID FROM customers WHERE CustomerID = {customer_id}'
        cursor.execute(sql_query)
        records = cursor.fetchall()
        if len(records) > 0:
            print('That customer already exists, please choose a new option.')
        # menu()
        else:
            return
    except mysql.connector.Error as error:
        print('Failed {}'.format(error))
    # menu()
