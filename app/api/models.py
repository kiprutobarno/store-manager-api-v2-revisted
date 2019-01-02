from passlib.hash import pbkdf2_sha256 as sha256
from manage import db


class User:
    """ User model """
    
    def create_user(email, is_admin, password):
        """ This function saves user particulars in the users table """
        conn=db()
        user = {
            "email": email,
            "is_admin": is_admin,
            "password": password
        }
        query=""" INSERT INTO users(email, is_admin, password) VALUES(%(email)s, %(is_admin)s, %(password)s) """

        cursor=conn.cursor()
        cursor.execute(query, user)
        conn.commit()
        return user

    def get_users():
        """This function returns particulars of all users in users table"""
        conn=db()
        cursor=conn.cursor()
        cursor.execute("""SELECT user_id, email, is_admin, date_created FROM users""")
        data=cursor.fetchall()
        users=[]
        for i, items in enumerate(data):
            user_id, email, is_admin, date_created=items
            user=dict(
                user_id=int(user_id),
                email=email,
                is_admin=bool(is_admin),
                date_created=date_created
            )
            users.append(user)
        return users

    def get_specific_user(user_id):
        """This method returns particulars of a specific user in users table"""
        conn=db()
        cursor=conn.cursor()
        cursor.execute("""SELECT user_id, email, is_admin, date_created FROM users WHERE user_id={}""".format(user_id))
        users=[]
        for i, items in enumerate(cursor.fetchall()): 
            user_id, email, is_admin, date_created=items
            user=dict(
                user_id=int(user_id),
                email=email,
                is_admin=bool(is_admin),
                date_created=date_created
            )
            users.append(user)
        return users

    def search(email):
        """ This function returns True if an email exists in the database."""
        conn=db()
        cursor=conn.cursor()
        cursor.execute("""SELECT * FROM users WHERE email='%s'"""%(email))
        data=cursor.fetchall() #tuple
        if len(data)>0:
            return True

    def login(email, password):
        """ This function verifies user password and returns the user's is_admin status """
        conn=db()
        cursor=conn.cursor()
        cursor.execute("""SELECT * FROM users  WHERE email='%s'"""%(email))
        hashes=cursor.fetchone() # returns a tuple
        if User.verify_hash(password, hashes[3]):
            return hashes

    @staticmethod
    def generate_hash(password):
        return sha256.hash(password)

    @staticmethod
    def verify_hash(password, hash):
        return sha256.verify(password, hash)

class Product:
    """Product model"""

    def create_product(product_name, category, quantity, price):
        """This function creates and saves product details in the products table"""
        conn=db()
        product = {
            "product_name": product_name,
            "category": category,
            "quantity": quantity,
            "unit_price":price
        }

        query=""" INSERT INTO products(product_name, category, quantity, unit_price) VALUES(%(product_name)s, %(category)s, %(quantity)s, %(unit_price)s) """
        cursor=conn.cursor()
        cursor.execute(query, product)
        conn.commit()
        return product

    def get_products():
            """This method returns particulars of all products in products table"""
            conn=db()
            cursor=conn.cursor()
            cursor.execute("""SELECT product_id, product_name, category, quantity, unit_price, date_created FROM products ORDER BY product_id ASC""")
            data=cursor.fetchall()
            rows=[]
            for i, items in enumerate(data):
                product_id, product_name, category, quantity, unit_price, date_created=items
                product=dict(
                    product_id=int(product_id),
                    product_name=product_name,
                    category=category,
                    quantity=quantity,
                    unit_price=unit_price,
                    date_created=date_created
                )
                rows.append(product)
            return rows

    def update_product(product_name, category, quantity, price, product_id):
            """ This function updates particulars of a specific product in the products table"""
            conn=db()
            cursor=conn.cursor()
            cursor.execute("UPDATE products SET product_name=%s, category=%s,quantity=%s, unit_price=%s WHERE product_id={}".format(product_id), (product_name, category, quantity, price))
            return conn.commit()

    def get_specific_product(product_id):
            """This function returns  the particulars of a specific product from products table"""
            conn=db()
            cursor=conn.cursor()
            cursor.execute("""SELECT product_id, product_name, category, quantity, unit_price, date_created FROM products WHERE product_id={}""".format(product_id))
            data=cursor.fetchall()
            products=[]
            for i, items in enumerate(data):
                product_id, product_name, category, quantity, unit_price, date_created=items
                product=dict(
                    product_id=int(product_id),
                    product_name=product_name,
                    category=category,
                    quantity=quantity,
                    unit_price=unit_price,
                    date_created=date_created
                )
                products.append(product) 
                if len(products)>0:
                    return product

    def delete(product_id):
        """This function deletes a product entry in the database"""
        conn=db()
        cursor=conn.cursor()
        cursor.execute("""DELETE FROM products WHERE product_id={}""".format(product_id))
        return conn.commit()

    def search(product_name, category):
        """ This function returns True if an email exists in the database."""
        conn=db()
        cursor=conn.cursor()
        cursor.execute("""SELECT product_id, product_name, category, quantity, unit_price, date_created FROM products WHERE product_name=%s AND category=%s""", (product_name, category))
        data=cursor.fetchall() #tuple
        if len(data)>0:
            return True

class Sale:
    """Sale Model"""
    
    def create_sale(product_id, quantity):
        conn=db()
        cursor=conn.cursor()
        cursor.execute("""SELECT * FROM products WHERE product_id={}""".format(product_id))
        data=cursor.fetchone()
        if data[3]>=quantity:
            price=data[4]
            cost=price * quantity
            stock=data[3]-int(quantity)

            sale = {
                "product_id": product_id,
                "product_name": data[1],
                "price": price,
                "quantity": quantity,
                "cost": price * quantity
            }
            query=""" INSERT INTO sales(product_id, product_name, price, quantity, cost) VALUES(%(product_id)s, %(product_name)s, %(price)s, %(quantity)s, %(cost)s) """
            cursor.execute(query, sale)
            cursor.execute("UPDATE products SET quantity={} WHERE product_id={}".format(stock, product_id))
            conn.commit()
            return sale

    def get_sales():
            """This method returns particulars of all items in sales table"""
            conn=db()
            cursor=conn.cursor()
            cursor.execute("""SELECT * FROM sales ORDER BY sale_id ASC""")
            data=cursor.fetchall()
            rows=[]
            for i, items in enumerate(data):
                sale_id, product_id, product_name, price, quantity, cost, time=items
                product=dict(
                    sale_id=int(sale_id),
                    product_id=int(product_id),
                    product_name=product_name,
                    price=price,
                    quantity=quantity,
                    cost=cost,
                    time=time
                )
                rows.append(product)
            return rows
    def get_specific_sale(sale_id):
            """This function returns  the particulars of a specific sale from sales table"""
            conn=db()
            cursor=conn.cursor()
            cursor.execute("""SELECT * FROM sales WHERE sale_id={}""".format(sale_id))
            data=cursor.fetchall()
            sales=[]
            for i, items in enumerate(data):
                sale_id, product_id, product_name, price, quantity, cost, time=items
                sale=dict(
                    sale_id=int(sale_id),
                    product_id=int(product_id),
                    product_name=product_name,
                    price=price,
                    quantity=quantity,
                    cost=cost,
                    time=time
                )
                sales.append(sale) 
                if len(sales)>0:
                    return sale

class Blacklist:
    """Token blacklist model"""

    def revoke_token(token, token_type, admin, issued_at, expires_at):
        """This function revokes and stores the revoked token in the blacklist table when user logs out"""
        conn=db()
        token = {
            "token": token,
            "token_type": token_type,
            "admin":admin,
            "issued_at":issued_at,
            "expires_at":expires_at
        }
        
        query="""INSERT INTO blacklist(token, token_type, admin, issued_at, expires_at) VALUES(%(token)s, %(token_type)s, %(admin)s, %(issued_at)s, %(expires_at)s) """

        cursor=conn.cursor()
        cursor.execute(query, token)
        conn.commit()
        return True

    def search(token):
        """This function returns True if a token exists in the blacklist table """
        conn=db()
        cursor=conn.cursor()
        cursor.execute(""" SELECT token from blacklist WHERE token='%s'"""%(token), token)
        if len(cursor.fetchall())>0:
            return True
