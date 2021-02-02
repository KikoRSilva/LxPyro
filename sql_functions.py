import sqlite3 as sql

# CONSTANTS
DATABASE = 'data/database.db'

# CONNECT TO SQLITE3 DATABASE
connection = sql.connect(DATABASE)
cursor = connection.cursor()

cursor.execute("SELECT * FROM Customer")

"""
    This function adds a customer to our DB to the Customer Table!
    The customer id auto-increments
    Arguments:
        -   Name of the customer
        -   Age of the customer
        -   Address of the customer
"""
def add_customer(name, age, address):
    cursor.execute(
        """
            INSERT INTO Customer VALUES(NULL,?,?,?,NULL)
        """,
        (name, age, address)
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
def add_product(name, price_per_unit, basic_unit, limited, stock, active_for_sale, image_url):
    cursor.execute(
        """
            INSERT INTO Product VALUES(NULL,?,?,?,?,?,?,?)
        """,
        (name, price_per_unit, basic_unit, limited, stock, active_for_sale, image_url)
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
def register_Sale(time_created, date_to_deliver, sale_amount, sale_amount_paid, customer_id):
    cursor.execute(
        """
            INSERT INTO Sale VALUES(NULL,?,?,?,?,?)
        """,
        (time_created, date_to_deliver, sale_amount,sale_amount_paid,customer_id)
    )
    cursor.commit()


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
def register_sale_item(quantity_sold, price_per_unit, price, sale_id, product_id):
    cursor.execute(
        """
            INSERT INTO Sale VALUES(NULL,?,?,?,?,?)
        """,
        (quantity_sold, price_per_unit, price, sale_id, product_id)
    )
    cursor.commit()


"""
    This functions saves the status of the sale!
    Arguments:
        -   Sale ID
        -   Status of the sale
"""
def register_sale_status(sale_id, status):
    cursor.execute(
        """
            INSERT INTO Sale_Status VALUES(?,?)
        """,
        (sale_id, status)
    )
    cursor.commit()


"""
    This function adds the product to the Stock table!
    Arguments:
        -   Product iD
        -   Quantity of the product to store
        -   Time updated
"""
def add_stock(product_id, stock, time):
    cursor.execute(
        """
            INSERT INTO Stock VALUES(?,?,?)
        """,
        (product_id, stock, time)
    )
    cursor.commit()


for row in cursor.execute('SELECT * FROM Customer'):
    print(row)
