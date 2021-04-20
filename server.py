from flask import Flask, render_template, redirect, request, session, url_for
import hashlib
from credentials import password, secretKey
from database import *

app = Flask(__name__,template_folder='templates')
app.secret_key = secretKey

# get Login details from database
def getLoginDetails():
    if 'email' not in session:
        loggedIn = False
        firstName = ''
        noOfItems = 0
    else:
        loggedIn = True
        query = f"SELECT User_ID, First_name FROM user WHERE Email = '{session['email']}'"
        data = execute_read_query(connection, query)
        userID, firstName = data[0][0], data[0][1]
        query = f"SELECT count(product_ID) FROM cart WHERE user_ID = '{userID}'"
        data = execute_read_query(connection, query)
        noOfItems = data[0][0]
    return (loggedIn, firstName, noOfItems)

# Convert list to tuples to a list
def email_list(emails):
    a = []
    for i in emails:
        a.append(i[0])
    return a

# check if credentials provided are valid or not
def valid_credentials(email, password):
    query = f"SELECT password FROM user WHERE email = '{email}'"
    data = execute_read_query(connection, query)
    if data and data[0][0] == hashlib.md5(password.encode()).hexdigest():
        return True
    return False

# Home page
@app.route("/")
def index():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    else:
        loggedIn, firstName, noOfItems = getLoginDetails()
        return render_template('index.html',firstName = firstName,loggedIn = loggedIn , noOfItems = noOfItems)

# catalog
@app.route("/catalog")
def catalog():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    else:
        loggedIn, firstName, noOfItems = getLoginDetails()
        category = request.args.get('category').title()
        # query = f"call category('{category}')"
        query = f"SELECT * FROM product WHERE category = '{category}'" 
        data = execute_read_query(connection, query)
        return render_template('catalog.html',firstName = firstName,loggedIn = loggedIn , noOfItems = noOfItems, itemData = data, category= category)

# Product Page
@app.route("/productDescription")
def productDescription():
    loggedIn, firstName, noOfItems = getLoginDetails()
    productId = request.args.get('productId')
    query = f"SELECT * FROM product WHERE Product_ID = {productId}"
    data = execute_read_query(connection, query)
    data = data[0]
    return render_template('product.html', data=data, firstName = firstName, loggedIn = loggedIn, noOfItems = noOfItems,)
    
# add to cart
@app.route("/addToCart")
def addToCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    else:
        productId = int(request.args.get('productId'))
        query = f"SELECT User_ID FROM user WHERE Email = \'{session['email']}\'"
        data = execute_read_query(connection, query)
        userId = data[0][0]
        query = f"CALL user_cart({productId}, {userId})"
        execute_query(connection, query)
        return redirect(url_for('index'))

# Cart
@app.route("/cart")
def cart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    query = f"SELECT User_ID FROM user WHERE Email = '{email}'"
    data = execute_read_query(connection, query)
    userId = data[0][0]
    query = f"SELECT product.product_ID, product.name, product.price, product.image, cart.quantity FROM product, cart WHERE product.product_ID = cart.product_Id AND cart.user_Id = '{userId}'"
    products = execute_read_query(connection, query)
    # return str(data)
    totalPrice = 0
    for row in products:
        totalPrice += ( row[2] * row[4])
    return render_template('cart.html', products=products, totalPrice=totalPrice, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

# checkout
@app.route("/payment")
def payment():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    else:
        email = session['email']
        query = f"SELECT User_ID FROM user WHERE Email = '{email}'"
        data = execute_read_query(connection, query)
        userId = data[0][0]
        query = f'INSERT INTO SALES (quantity, price, user_id, product_id) SELECT cart.quantity, product.price, cart.user_id, cart.product_id FROM cart INNER JOIN product ON cart.product_id = product.product_ID AND User_ID = "{userId}"'
        data = execute_query(connection, query)
        query = f'DELETE FROM cart where USER_id = "{userId}"'
        data = execute_query(connection, query)
        return render_template('paymentsuccessful.html')

# my orders
@app.route("/myOrders")
def myOrders():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    email = session['email']
    query = f"SELECT User_ID FROM user WHERE Email = '{email}'"
    data = execute_read_query(connection, query)
    userId = data[0][0]
    query = f'SELECT product.product_Id, product.name, sales.total_amount, product.image, sales.invoice_no, sales.quantity, sales.price FROM product, sales WHERE product.product_Id = sales.product_Id AND sales.user_Id = "{userId}"'
    items = execute_read_query(connection, query)
    return render_template("myOrders.html", items = items, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

# remove from cart
@app.route("/removeFromCart")
def removeFromCart():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    email = session['email']
    productId = int(request.args.get('productId'))
    query = f"SELECT User_ID FROM user WHERE Email = '{email}'"
    data = execute_read_query(connection, query)
    userId = data[0][0]
    query = f"DELETE FROM cart WHERE User_ID = '{userId}' AND Product_ID = '{productId}'"
    execute_query(connection, query)
    return redirect(url_for('cart'))

# Login
@app.route("/loginForm")
def loginForm():
    if 'email' in session:
        return redirect(url_for('index'))
    else:
        return render_template('login.html', error='')

@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if valid_credentials(email, password):
            session['email'] = email
            return redirect(url_for('index'))

        error = 'Invalid Email / Password'
        return render_template('login.html', error=error)

# Registration
@app.route("/registerationForm")
def registrationForm():
    if 'email' in session:
        return redirect(url_for('index'))
    return render_template("register.html")

@app.route("/register", methods = ['GET', 'POST'])
def register():
    if 'email' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Parse form data
        firstName = request.form['firstName'].title()    
        lastName = request.form['lastName'].title()
        email = request.form['email']
        password = request.form['password']
        house = request.form['house']
        city = request.form['city']
        state = request.form['state']
        pincode = int(request.form['pincode'])

        query = "SELECT email FROM user"
        emails = execute_read_query(connection, query)
        emails = email_list(emails)
        
        if email in emails:
            return render_template("register.html", error="Account already exists")
        else:
            query = f"CALL insertUser ('{firstName}', '{lastName}', '{email}', '{hashlib.md5(password.encode()).hexdigest()}', '{house}', '{city}','{state}','{pincode}')"
            execute_query(connection, query)

        session['email'] = email
        return redirect(url_for('index'))

@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    connection = create_connection("localhost", "root", password, "ecart")
    app.run(debug = True)