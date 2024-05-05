from flask import Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import sqlite3

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'super-secret'  # Change this to a secure key in production
jwt = JWTManager(app)
DATABASE = 'database.db'

'''
create_table() is for creating table if it does not exist in sqlite
'''

def create_table():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY, title TEXT, description TEXT, price REAL)''')
    conn.commit()
    conn.close()

create_table()

def is_valid_product(data):
    if 'title' not in data or 'description' not in data or 'price' not in data:
        return False
    if not isinstance(data['title'], str) or not isinstance(data['description'], str) or not isinstance(data['price'], (int, float)):
        return False
    return True

'''
route           /login
description     login to create access_token in jwt
access          public
parameter       none
method          POST
'''

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    # You can add your own authentication logic here (e.g., check credentials against a database)
    if username == 'admin' and password == 'password':
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    else:
        return jsonify({'message': 'Invalid credentials'}), 401


'''
route           /products
description     get all the products present in database
access          public
parameter       none
method          GET
'''

@app.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT * FROM products')
    products = c.fetchall()
    conn.close()
    return jsonify(products)


'''
route           /products/<int:product_id>
description     get particular product based on the product id
access          public
parameter       product_id
method          GET
'''

@app.route('/products/<int:product_id>', methods=['GET'])
@jwt_required()
def get_product(product_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    limit = request.args.get('limit', 10, type=int)  # Default limit to 10 if not provided
    skip = request.args.get('skip', 0, type=int)  # Default skip to 0 if not provided

    c.execute('SELECT * FROM products WHERE id = ?', (product_id,))
    product = c.fetchone()
    conn.close()
    if product:
        return jsonify(product)
    else:
        return jsonify({'error': 'Product not found'}), 404


'''
route           /products
description     create a new product
access          public
parameter       NONE
method          POST
'''

@app.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.json
    if not is_valid_product(data):
        return jsonify({'message': 'Missing Some data check again'}), 400
    title = data.get('title')
    description = data.get('description')
    price = data.get('price')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT INTO products (title, description, price) VALUES (?, ?, ?)', (title, description, price))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product created successfully'})


'''
route           /products/<int:product_id>
description     Updtae a product based on product_id
access          public
parameter       product_id
method          PUT
'''

@app.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    data = request.json
    if not is_valid_product(data):
        return jsonify({'message': 'Missing Some data check again'}), 400
    title = data.get('title')
    description = data.get('description')
    price = data.get('price')
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('UPDATE products SET title=?, description=?, price=? WHERE id=?', (title, description, price, product_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product updated successfully'})


'''
route           /products/<int:product_id>
description     Delete a product based on product_id
access          public
parameter       product_id
method          DELETE
'''

@app.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('DELETE FROM products WHERE id=?', (product_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Product deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
