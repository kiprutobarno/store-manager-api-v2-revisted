import os
import psycopg2

url = os.environ.get('DATABASE_URL')

def connection(url):
    """This function creates a connection to the databse"""
    return psycopg2.connect(url)

def db():
    """This function returns a database connection object"""
    return connection(url)

def create_tables():
    """This function creates tables in the database"""
    conn = connection(url)
    cursor = conn.cursor()
    queries = create_queries()
    for query in queries:
        cursor.execute(query)
    conn.commit()

def destroy_tables():
    """This function destroys tables in the database"""
    conn = connection(url)
    cursor = conn.cursor()
    statements = destroy_queries()
    for statement in statements:
        cursor.execute(statement)
    conn.commit()


def destroy_queries():
    delete_users = """drop table if exists users;"""
    delete_products = """drop table if exists products;"""
    delete_sales = """drop table if exists sales;"""
    delete_blacklist = """drop table if exists blacklist;"""

    statements=[delete_users, delete_products, delete_sales, delete_blacklist]
    return statements


def create_queries():
    """This function returns a list of 'create table' queries"""
    users = """create table if not exists users(user_id serial primary key not null, 
                    email varchar(50) not null,
                    is_admin boolean default false,
                    password varchar(200) not null,
                    date_created TIMESTAMP NULL DEFAULT NOW() );"""
    products = """create table if not exists products(
                    product_id serial primary key not null, 
                    product_name varchar(50) not null, 
                    category varchar(50) not null, 
                    quantity int not null, 
                    unit_price float not null,
                    date_created TIMESTAMP NULL DEFAULT NOW() );"""
    blacklist = """create table if not exists blacklist(token_id serial primary key not null, 
                    token varchar(500) not null,
                    token_type varchar(50) not null,
                    admin varchar(50) not null,
                    issued_at varchar(50) not null,
                    expires_at varchar(50) not null,
                    blacklisted_at TIMESTAMP NULL DEFAULT NOW() );"""
    sales = """create table if not exists sales(sale_id serial primary key not null, 
                    product_id int not null,
                    product_name varchar(50) not null,
                    price int not null,
                    quantity int not null,
                    cost float not null,
                    time TIMESTAMP NULL DEFAULT NOW() );"""

    queries=[users, products, blacklist, sales]
    return queries