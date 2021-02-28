import sqlite3 as sql
from app import DATABASE
"""
    This function adds a customer to our DB to the Customer Table!
    The customer id auto-increments
    Arguments:
        -   Name of the customer
        -   Age of the customer
        -   Address of the customer
"""
def add_customer(cursor, connection, name, phone, insta, age, address):
    cursor.execute(
        """
            INSERT INTO Customer VALUES(NULL,?,?,?,?,?,?)
        """,
        (name, phone, insta, age, address, 0)
    )
    connection.commit()


"""
    This function adds a product to our DB to the Product Table!
    The product id auto-increments
    Arguments:
        -   Name of the product
        -   Price of each product unit
        -   Product unit (eggs, kilo, meters...)
        -   If the product has limited stock or not
        -   Current amount of product units in stock
        -   If is active for sale or not
        -   Local path to image of the product
"""
def add_product(cursor, connection, name, price_per_unit, basic_unit, limited, stock, active_for_sale, image_url,
                description):


    cursor.execute(
        """
            INSERT INTO Product VALUES(NULL,?,?,?,?,?,?,?,?)
        """,
        (name, price_per_unit, basic_unit, limited, stock, active_for_sale, image_url, description)
    )
    connection.commit()


"""
    This function register a sale to the DB Sale Table!
    The sale id auto-increments.
    Arguments:
        -   Time that the sale was registered
        -   Date to deliver the sale
        -   Amount to pay for the sale
        -   Amount paid of the sale
        -   Customer ID that made the sale
"""
def register_sale_sql(cursor, connection, time_created, date_to_deliver, sale_amount, sale_amount_paid, customer_id, address):
    cursor.execute(
        """
            INSERT INTO Sale VALUES(NULL,?,?,?,?,?,?)
        """,
        (time_created, date_to_deliver, sale_amount, sale_amount_paid, customer_id, address)
    )
    connection.commit()


"""
    This function register a sale item to the DB Sale_Item Table!
    The sale item id auto-increments.
    Arguments:
        -   Quantity of the product that was sold
        -   Price of each product unit  
        -   Price of the product    (just to save the product price of that day)
        -   Sale ID
        -   Product ID
"""
def register_sale_item(cursor, connection, quantity_sold, price, sale_amount, sale_id, product_id):
    cursor.execute(
        """
            INSERT INTO Sale_Item VALUES(NULL,?,?,?,?,?)
        """,
        (quantity_sold, price, sale_amount, sale_id, product_id)
    )
    connection.commit()


"""
    This functions saves the status of the sale!
    Arguments:
        -   Sale ID
        -   Status of the sale
"""


def register_sale_status(cursor, connection, sale_id, status):
    cursor.execute(
        """
            INSERT INTO Sale_Status VALUES(?,?)
        """,
        (sale_id, status)
    )
    connection.commit()


"""
    This function adds the product to the Stock table!
    Arguments:
        -   Product iD
        -   Quantity of the product to store
        -   Time updated
"""


def add_stock(cursor, connection, product_id, stock, time):
    cursor.execute(
        """
            INSERT INTO Stock VALUES(?,?,?)
        """,
        (product_id, stock, time)
    )
    connection.commit()


"""
    This function returns a product list from our DB
    Arguments:
        -   Cursor
        -   Connection
        -   Name of the product
        -   Price of each product unit
        -   Product unit (eggs, kilo, meters...)
        -   If the product has limited stock or not
        -   Current amount of product units in stock
        -   If is active for sale or not
        -   Local path to image of the product
"""

# Get a list with the product's name
def get_products_list(cursor, connection):
    cursor.execute(
        """
            SELECT DISTINCT name FROM Product
        """
    )
    connection.commit()
    return cursor.fetchall()

# Get a list with the Customer's name
def get_customers_list(cursor, connection):
    cursor.execute(
        """
            SELECT DISTINCT name FROM Customer
        """
    )
    connection.commit()
    return cursor.fetchall()

# Get a list of all products registered
def get_all_products(cursor, connection):
    cursor.execute("SELECT * FROM Product")
    return cursor.fetchall()


def get_product_price(cursor, connection, name):
    cursor.execute("SELECT DISTINCT price_per_unit FROM Product WHERE name=?", (name,))
    return cursor.fetchone()

def get_product_stock(cursor, connection, product):
    cursor.execute("SELECT DISTINCT in_stock FROM Product WHERE name=?", (product,))
    return cursor.fetchone()

def get_sale_id(cursor, connection, time):
    cursor.execute("SELECT DISTINCT id FROM Sale WHERE time_created=?", (time,))
    return cursor.fetchone()

def get_product_id(cursor, connection, product):
    cursor.execute("SELECT DISTINCT id FROM Product WHERE name=?", (product,))
    return cursor.fetchone()

def get_customer_id(cursor, connection, customer):
    cursor.execute("SELECT DISTINCT id FROM Customer WHERE name=?", (customer,))
    return cursor.fetchone()

def update_product_stock(cursor, connection, id, product, quantity):
    current_stock = get_product_stock(cursor, connection, product)[0]
    total = current_stock - quantity
    cursor.execute("UPDATE Product SET in_stock=? WHERE id=?", (total, id))
    connection.commit()

def set_sale_status(cursor, connection, status):
    cursor.execute(
        """
            INSERT INTO Sale_Status VALUES (NULL, ?)
        """,
        (status,)
    )
    connection.commit()

def update_customer_sale_amount(cursor, connection, customer_id, sale_amount):
    cursor.execute("UPDATE Customer SET sales_amount=sales_amount+? WHERE id=?", (sale_amount, customer_id))
    connection.commit()
