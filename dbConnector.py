import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode


def get_db_connection():
	try:
		connection = mysql.connector.connect(host='localhost',
											database='northwind',
											user='root',
											password='Sknapper4.0')
		return connection
	except mysql.connector.Error as error:
		print('Failed to connnect to database {}'.format(error))


def close_db_connection(connection):
	try:
		connection.close()
	except mysql.connector.Error as error:
		print('Failed to close database connection {}'.format(error))


def read_db_version():
	try:
		connection = get_db_connection()
		db_info = connection.get_server_info()
		print('Connected to MySQL database. MySQL Server version is ' , db_info)
		cursor = connection.cursor()
		cursor.execute('Select database();')
		record = cursor.fetchone()
		print('You\'re connected to -', record)
		close_db_connection(connection)
	except mysql.connector.Error as error:
		print('Failed to read database version {}'.format(error))


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


def add_customer():
	try:
		connection = get_db_connection()
		cursor = connection.cursor()
		value_string = get_customer_tbl_vals()
		sql_query = 'SELECT * FROM customers'
		cursor.execute(sql_query)
		records = cursor.fetchall()

		for row in records:
			print(row)
	except mysql.connector.Error as error:
		print('Failed {}'.format(error))


def get_customer_tbl_vals()
	
	return '({customer_id}, {company_name},{contact_name},',
	'{contact_title},{address}, {city}, {region}, {postal_code},',
	' {country}, {phone}, {fax})'
