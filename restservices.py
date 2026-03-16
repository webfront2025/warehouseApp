from flask import Flask, request
from flask_restful import Api, Resource
from flasgger import Swagger
from flask_cors import CORS
from datetime import datetime
from models import ValidateProduct, ValidateOrder, ValidateTransaction

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
api = Api(app)
swagger = Swagger(app)


# Test data before database implementation
# Once we have the database implemented, it can be tied in by replacing this
products = [
    {
        'id': 1, 
        'name': 'Laptop Pro 15"', 
        'description': 'High-performance laptop with 16GB RAM and 512GB SSD',
        'category': 'Elektronik', 
        'quantity': 15, 
        'price': 8999.00,
        'location': 'Lager A',
        'supplier': 'TechSupply Denmark'
    },
    {
        'id': 2, 
        'name': 'Trådløs Mus', 
        'description': 'Ergonomisk trådløs mus med lang batterilevetid',
        'category': 'Elektronik', 
        'quantity': 50, 
        'price': 299.00,
        'location': 'Lager B',
        'supplier': 'TechSupply Denmark'
    },
    {
        'id': 3, 
        'name': 'Kontorstol Premium', 
        'description': 'Ergonomisk kontorstol med lændestøtte',
        'category': 'Møbler', 
        'quantity': 8, 
        'price': 2499.00,
        'location': 'Lager C',
        'supplier': 'OfficeMester A/S'
    },
    {
        'id': 4, 
        'name': 'Kaffe bønner 1kg', 
        'description': 'Premium arabica kaffe bønner fra Colombia',
        'category': 'Fødevarer', 
        'quantity': 25, 
        'price': 159.00,
        'location': 'Lager D',
        'supplier': 'Nordic Coffee Co.'
    },
    {
        'id': 5, 
        'name': 'Vinterjakke', 
        'description': 'Vandtæt og varm vinterjakke i størrelse M',
        'category': 'Tøj', 
        'quantity': 12, 
        'price': 799.00,
        'location': 'Lager A',
        'supplier': 'Fashion Nordic'
    }
]
orders = [
    {'id': 1, 'product_id': 1, 'quantity': 1, 'date': datetime.now().isoformat()}
]
transactions = [
    {'id': 1, 'type': 'sale', 'product_id': 1, 'quantity': 1, 'date': datetime.now().isoformat()}
]

### REST SERVICES FOR PRODUCTS
# Class for functions relating to all products (GET, POST)
class ProductREST(Resource):
    def get(self):
        """
        Get all products with optional filtering
        ---
        parameters:
          - in: query
            name: category
            type: string
            required: false
            description: Filter by product category
          - in: query
            name: min_price
            type: number
            required: false
            description: Minimum price filter
          - in: query
            name: max_price
            type: number
            required: false
            description: Maximum price filter
          - in: query
            name: min_quantity
            type: integer
            required: false
            description: Minimum quantity filter
          - in: query
            name: location
            type: string
            required: false
            description: Filter by location
          - in: query
            name: supplier
            type: string
            required: false
            description: Filter by supplier
        responses:
          200:
            description: Returns list of filtered products
        """
        filtered_products = products.copy()
        
        # Apply filters
        if request.args.get('category'):
            category = request.args.get('category')
            filtered_products = [p for p in filtered_products if p.get('category', '').lower() == category.lower()]
        
        if request.args.get('min_price'):
            min_price = float(request.args.get('min_price'))
            filtered_products = [p for p in filtered_products if p.get('price', 0) >= min_price]
        
        if request.args.get('max_price'):
            max_price = float(request.args.get('max_price'))
            filtered_products = [p for p in filtered_products if p.get('price', 0) <= max_price]
        
        if request.args.get('min_quantity'):
            min_quantity = int(request.args.get('min_quantity'))
            filtered_products = [p for p in filtered_products if p.get('quantity', 0) >= min_quantity]
        
        if request.args.get('location'):
            location = request.args.get('location')
            filtered_products = [p for p in filtered_products if p.get('location', '').lower() == location.lower()]
        
        if request.args.get('supplier'):
            supplier = request.args.get('supplier')
            filtered_products = [p for p in filtered_products if p.get('supplier', '').lower() == supplier.lower()]
        
        return filtered_products, 200
    
    def post(self):
        """
        Create a new product
        ---
        parameters:
            -   in: body
                name: product
                required:
                schema:
                    type: object
                    required:
                        - name
                        - category
                        - quantity
                        - price
                    properties:
                        name:
                            type: string
                        category:
                            type: string
                        quantity:
                            type: integer
                        price:
                            type: number
        responses:
          201:
            description: New product created
          422:
            description: Invalid data (quantity must be INT, price must be a number)
        """
        data = request.json

        currentID = products[-1]['id'] + 1
        newProduct = {
            'id': currentID, 
            'name': data['name'], 
            'description': data.get('description', ''),
            'category': data['category'], 
            'quantity': data['quantity'], 
            'price': data['price'],
            'location': data.get('location', ''),
            'supplier': data.get('supplier', '')
            }
        
        if ValidateProduct(newProduct):
            products.append(newProduct)
            return newProduct, 201
        else: return {'message': 'Unable to parse data'}, 422
    
# Class for functions related to a single product (GET[id], PUT, DELETE)
class ProductIDRest(Resource):
    def get(self, id):
        """
        Find a specific product based on its ID
        ---
        parameters:
          - in: path
            name: id
            type: integer
            required: true
        responses:
          200:
            description: Returns product
          404:
            description: Product not found
        """
        for x in products:
            if x['id'] == id:
                return x, 200
        return {'message': 'Product not found'}, 404
    
    def put(self, id):
        """
        Update an existing product
        ---
        parameters:
          - in: path
            name: id
            type: integer
            required: true
          - in: body
            name: body
            required: true
            schema:
                type: object
                required:
                    - name
                    - category
                    - quantity
                    - price
                properties:
                    name:
                        type: string
                    category:
                        type: string
                    quantity:
                        type: integer
                    price:
                        type: number
        responses:
          200:
            description: Successfully updated the product
          404:
            description: Product not found
        """
        data = request.json

        if not ValidateProduct(data):
            return {'message': 'Invalid data'}, 422

        for x in products:
            if x['id'] == id:
                x.update(data)
                return x, 200
        return {'message': 'Product not found'}, 404
    
    def delete(self, id):
        """
        Delete a product
        ---
        parameters:
          - in: path
            name: id
            type: integer
            required: true
        responses:
          200:
            description: Successfully deleted the product
          404:
            description: Product not found
        """
        for i, x in enumerate(products):
            if x['id'] == id:
                dProduct = products.pop(i)
                return dProduct, 200
        return {'message': 'Product not found'}, 404

### REST SERVICES FOR ORDERS
# Class for functions relating to all orders (GET, POST)
class OrderREST(Resource):
    def get(self):
        """
        Get all orders
        ---
        responses:
          200:
            description: Returns list of orders
        """
        return orders, 200    
    
    def post(self):
        """
        Create a new order
        ---
        parameters:
            -   in: body
                name: order
                required:
                schema:
                    type: object
                    required:
                        - product_id
                        - quantity
                    properties:
                        product_id:
                            type: integer
                        quantity:
                            type: integer
        responses:
          201:
            description: New product created
          404:
            description: Cannot find product tied to product_id
          422:
            description: Invalid data (quantity must be INT)
        """
        data = request.json
        potentialID = data['product_id']
        
        if ProductIDRest.get(self, potentialID)[1] == 404:
            return {'message': 'Cannot make an order for product that does not exist'}, 404

        currentID = orders[-1]['id'] + 1
        newOrder = {
            'id': currentID,
            'product_id': data['product_id'],
            'quantity': data['quantity'], 
            'date': datetime.now().isoformat()
            }
        
        if ValidateOrder(newOrder):
            orders.append(newOrder)
            return newOrder, 201
        else: return {'message': 'Unable to parse data'}, 422

# Class for functions related to a single order (GET[id], PUT, DELETE)
class OrderIDRest(Resource):
    def get(self, id):
        """
        Find a specific order based on its ID
        ---
        parameters:
          - in: path
            name: id
            type: integer
            required: true
        responses:
          200:
            description: Returns order
          404:
            description: Order not found
        """
        for x in orders:
            if x['id'] == id:
                return x, 200
        return {'message': 'Order not found'}, 404
    
    def put(self, id):
        """
        Update an existing order
        ---
        parameters:
          - in: path
            name: id
            type: integer
            required: true
          - in: body
            name: body
            required: true
            schema:
                type: object
                required:
                    - product_id
                    - quantity
                    - date
                properties:
                    product_id:
                        type: integer
                    quantity:
                        type: integer
                    date:
                        type: boolean
        responses:
          200:
            description: Successfully updated the order
          404:
            description: Order not found
        """
        data = request.json

        if not ValidateOrder(data):
            return {'message': 'Invalid data'}, 422

        for x in orders:
            if x['id'] == id:
                # The next few lines are to keep/change the order's DateTime
                # If input is True, then DateTime is updated to now
                # If input is False, then DateTime is left alone
                if data['date'] == True:
                    data['date'] = datetime.now().isoformat()
                else:
                    data['date'] = x['date']
                x.update(data)
                return x, 200
        return {'message': 'Order not found'}, 404
    
    def delete(self, id):
        """
        Delete an order
        ---
        parameters:
          - in: path
            name: id
            type: integer
            required: true
        responses:
          200:
            description: Successfully deleted the order
          404:
            description: Order not found
        """
        for i, x in enumerate(orders):
            if x['id'] == id:
                dOrder = orders.pop(i)
                return dOrder, 200
        return {'message': 'Order not found'}, 404

### REST SERVICES FOR TRANSACTIONS
# Class for functions relating to all transactions (GET, POST)
class TransactionREST(Resource):
    def get(self):
        """
        Get all transactions
        ---
        responses:
          200:
            description: Returns list of transactions
        """
        return transactions, 200    
    
    def post(self):
        """
        Create a new transaction
        ---
        parameters:
            -   in: body
                name: transaction
                required:
                schema:
                    type: object
                    required:
                        - type
                        - product_id
                        - quantity
                    properties:
                        type:
                            type: string
                        product_id:
                            type: integer
                        quantity:
                            type: integer
        responses:
          201:
            description: New product created
          404:
            description: Cannot find product tied to product_id
          422:
            description: Invalid data (quantity must be INT)
        """
        data = request.json
        potentialID = data['product_id']
        
        if ProductIDRest.get(self, potentialID)[1] == 404:
            return {'message': 'Cannot make a transaction for product that does not exist'}, 404

        currentID = transactions[-1]['id'] + 1
        newTransaction = {
            'id': currentID,
            'type': data['type'],
            'product_id': data['product_id'],
            'quantity': data['quantity'], 
            'date': datetime.now().isoformat()
            }
        
        if ValidateTransaction(newTransaction):
            transactions.append(newTransaction)
            return newTransaction, 201
        else: return {'message': 'Unable to parse data'}, 422

# Class for functions related to a single order (GET[id], PUT, DELETE)
class TransactionIDRest(Resource):
    def get(self, id):
        """
        Find a specific transaction based on its ID
        ---
        parameters:
          - in: path
            name: id
            type: integer
            required: true
        responses:
          200:
            description: Returns transaction
          404:
            description: Transaction not found
        """
        for x in transactions:
            if x['id'] == id:
                return x, 200
        return {'message': 'Order not found'}, 404
    
    def put(self, id):
        """
        Update an existing transaction
        ---
        parameters:
          - in: path
            name: id
            type: integer
            required: true
          - in: body
            name: body
            required: true
            schema:
                type: object
                required:
                    - type
                    - product_id
                    - quantity
                    - date
                properties:
                    type:
                        type: string
                    product_id:
                        type: integer
                    quantity:
                        type: integer
                    date:
                        type: boolean
        responses:
          200:
            description: Successfully updated the transaction
          404:
            description: Transaction not found
        """
        data = request.json

        if not ValidateTransaction(data):
            return {'message': 'Invalid data'}, 422

        for x in transactions:
            if x['id'] == id:
                # See Order's PUT function for explanation for these lines
                if data['date'] == True:
                    data['date'] = datetime.now().isoformat()
                else:
                    data['date'] = x['date']
                x.update(data)
                return x, 200
        return {'message': 'Transaction not found'}, 404
    
    def delete(self, id):
        """
        Delete a transaction
        ---
        parameters:
          - in: path
            name: id
            type: integer
            required: true
        responses:
          200:
            description: Successfully deleted the transaction
          404:
            description: Transaction not found
        """
        for i, x in enumerate(transactions):
            if x['id'] == id:
                dTransaction = transactions.pop(i)
                return dTransaction, 200
        return {'message': 'Transaction not found'}, 404

# Login endpoint
@app.route('/login', methods=['POST', 'OPTIONS'])
def login():
    """
    Simple login endpoint
    ---
    parameters:
      - in: body
        name: login
        required: true
        schema:
          type: object
          required:
            - username
            - password
          properties:
            username:
              type: string
            password:
              type: string
    responses:
      200:
        description: Login successful
      401:
        description: Invalid credentials
    """
    if request.method == 'OPTIONS':
        return '', 200
    
    print(f"Request method: {request.method}")
    print(f"Request data: {request.data}")
    print(f"Request JSON: {request.json}")
    
    try:
        data = request.json
        if not data:
            print("No JSON data received")
            return {'message': 'No JSON data received'}, 400
            
        username = data.get('username')
        password = data.get('password')
        
        print(f"Username: {username}, Password: {password}")
        
        # Simple authentication - in production, use proper password hashing
        if username == 'admin' and password == 'password':
            return {'token': 'fake-jwt-token'}, 200
        else:
            return {'message': 'Invalid credentials'}, 401
    except Exception as e:
        print(f"Error: {e}")
        return {'message': f'Error: {str(e)}'}, 400

# API routes
api.add_resource(ProductREST, '/products')
api.add_resource(ProductIDRest, '/products/<int:id>')
api.add_resource(OrderREST, '/orders')
api.add_resource(OrderIDRest, '/orders/<int:id>')
api.add_resource(TransactionREST, '/transactions')
api.add_resource(TransactionIDRest, '/transactions/<int:id>')

# Swagger tests are done through /apidocs
if __name__ == '__main__':
    app.run(debug = True)