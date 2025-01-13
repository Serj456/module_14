import sqlite3

connection = sqlite3.connect('products.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    )
    
''')

def add_product(product_id, title, description, price):
    check_product = cursor.execute("SELECT * FROM Products WHERE id = ?", (product_id,))
    if check_product.fetchone() is None:
        cursor.execute(f'''
        INSERT INTO Products VALUES('{product_id}','{title}', '{description}', '{price}')
        ''')
    connection.commit()

def get_all_products(product_id):
    product_list = cursor.execute("SELECT * FROM Products")
    descr = ''
    for product in product_list:
        if product_id == product[0]:
            descr += f'{product[1]} | {product[2]} | {product[3]}'
    connection.commit()
    return descr


add_product(1, 'product 1', 'описание 1', 100)
add_product(2, 'product 2', 'описание 2', 200)
add_product(3, 'product 3', 'описание 3', 300)
add_product(4, 'product 4', 'описание 4', 400)



connection.commit()
