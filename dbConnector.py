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
        print('Connected to MySQL database. MySQL Server version is ', db_info)
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
        add_value_string = get_customer_tbl_vals()
        sql_query = f'INSERT INTO customers VALUES {add_value_string}'
        cursor.execute(sql_query)
        connection.commit()
    except mysql.connector.Error as error:
        print('Failed {}'.format(error))


def get_customer_tbl_vals():
    customer_id = input('Please enter the customer ID')
    customer_id = '"' + customer_id + '"'
    keep_going = check_customer_existence(customer_id)
    if not keep_going:
        print('That customer ID already exists')
        return
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
            return False
        else:
            return True
    except mysql.connector.Error as error:
        print('Failed {}'.format(error))


def add_order():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        add_value_string = get_orders_table_vals('orders')
        sql_query = f'INSERT INTO orders VALUES {add_value_string}'
        cursor.execute(sql_query)
        # connection.commit()
        add_value_string = get_orders_table_vals('order_details')
        sql_query = f'INSERT INTO order_details VALUES {add_value_string}'
        cursor.execute(sql_query)
    except mysql.connector.Error as error:
        print('Failed {}'.format(error))


def get_orders_table_vals(function_called):
    order_ID = get_highest_id('orders', 'OrderID') + 1
    customer_ID = input('Please enter the customerID\n>')
    customer_ID = '"' + customer_ID + '"'
    does_not_exist = check_customer_existence(customer_ID)
    if does_not_exist:
        print('That customer does not exist')
        return
    employee_ID = get_highest_id('orders', 'EmployeeID') + 1
    order_date = input('Please enter the order date. Like 1998-05-05 00:00:00\n>')
    print(order_date)
    required_date = input('Please enter the required date. Like 1998-05-05 00:00:00\n>')
    shipped_date = input('Please enter the shipped date. Like 1998-05-05 00:00:00\n>')
    ship_via = input('Please enter the shipper company code\n>')
    freight = input('Please enter the frieght\n>')
    ship_name = input('Please enter the shipper name\n>')
    ship_address = input('Please enter the shipper address\n>')
    ship_city = input('Please enter the shipper city\n>')
    ship_region = input('Please enter the shipper region\n>')
    ship_postal_code = input('Please enter the shipper postalcode\n>')
    ship_country = input('Please enter the shipper country\n>')
    order_details_id = get_highest_id('order_details', 'ID') + 1
    product_id = get_highest_id('order_details', 'ProductID') + 1
    unit_price = input('Please enter the unit price\n>')
    quantity = input('Please enter the quantity\n>')
    discount = input('Please enter the discount\n>')
    if function_called == 'orders':
        return f'({order_ID}, {customer_ID}, {employee_ID}, {order_date}, {required_date}, {shipped_date}, {ship_via}, {freight}, {str(ship_name)}, {str(ship_address)}, {str(ship_city)}, {str(ship_region)}, {ship_postal_code}, {ship_country})'
    elif function_called == 'order_details':
        return f'({order_details_id}, {order_ID}, {product_id}, {unit_price}, {quantity}, {discount})'


def get_highest_id(table, id_name):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql_query = f'SELECT MAX(%s) FROM %s' % (id_name, table)
        cursor.execute(sql_query)
        records = cursor.fetchall()
        return int(records[0][0])
    except mysql.connector.Error as error:
        print('Failed {}'.format(error))


def remove_order():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        order_id_to_remove = input('Please enter the orderID of the order you \nwould like to remove\n>')
        sql_query = f'DELETE FROM order_details WHERE OrderID = {order_id_to_remove}'
        cursor.execute(sql_query)
        sql_query = f'DELETE FROM orders WHERE OrderID = {order_id_to_remove}'
        cursor.execute(sql_query)
        connection.commit()
    except mysql.connector.Error as error:
        print('Failed {}'.format(error))


def print_pending_orders():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        sql_query = 'SELECT * FROM customers, orders WHERE customers.CustomerID IN (SELECT CustomerID FROM orders WHERE ShippedDate is NULL)'
        cursor.execute(sql_query)
        records = cursor.fetchall()
        for row in records:
            print(row)
    except mysql.connector.Error as error:
        print('Failed {}'.format(error))


def ship_order():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        order_to_ship = input('Enter the OrderID of the order you want to ship\n>')
        does_order_exist = check_if_order_id_exists(order_to_ship)
        if not does_order_exist:
            print('OrderID does not exist')
            return
        sql_query = f'SELECT Quantity, ProductID FROM order_details WHERE OrderID = %s' % order_to_ship
        cursor.execute(sql_query)
        records = cursor.fetchall()
        print(records)
        quantity = records[0][0]
        product_id = records[0][1]
        sql_query = f'UPDATE products SET UnitsInStock = UnitsInStock + %f WHERE ProductID = %s' % (quantity, product_id)
        cursor.execute(sql_query)
        connection.commit()
    except mysql.connector.Error as error:
        print('Failed {}'.format(error))


def check_if_order_id_exists(order_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        order_id = '"' + order_id + '"'
        sql_query = f'SELECT OrderID FROM orders WHERE OrderID = %s' % order_id
        cursor.execute(sql_query)
        records = cursor.fetchall()
        if len(records) > 0:
            return True
        else:
            return False
    except mysql.connector.Error as error:
        print('Failed {}'.format(error))


def restock():
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        product_id = input('Please enter the ProductId of the product you want to restock\n>')
        product_exists = check_products_existence(product_id)
        if not product_exists:
            print('That ProductID does not exist')
            return
        sql_query = f'SELECT ReorderLevel FROM products WHERE Discontinued <> "y" AND ProductID = %s' % product_id
        cursor.execute(sql_query)
        records = cursor.fetchall()
        reorder_quantity = records[0][0]
        sql_query = f'UPDATE products SET UnitsInStock = UnitsInStock + %f WHERE ProductID = %s' % (reorder_quantity, product_id)
        cursor.execute(sql_query)
        connection.commit()
    except mysql.connector.Error as error:
        print('Failed {}'.format(error))


def check_products_existence(product_id):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        product_id = '"' + product_id + '"'
        sql_query = f'SELECT ProductID FROM products WHERE ProductId = %s' % product_id
        cursor.execute(sql_query)
        records = cursor.fetchall()
        if len(records) > 0:
            return True
        else:
            return False
    except mysql.connector.Error as error:
        print('Failed {}'.format(error))
