from flask import Flask, render_template, request, redirect, session, url_for, flash  
from models import db, Product, Contact, User,Order
from config import Config

app = Flask(__name__)
app.config.from_object(Config)


db.init_app(app)


with app.app_context():
    db.create_all()

   
    for p in Product.query.all():
        if p.category == "spoon set":
            p.category = "spoon-set"
        elif p.category == "lunch box":
            p.category = "lunch-box"
        elif p.category == "frying pan":
            p.category = "frying-pan"
        elif p.category == "pressure cooker":
            p.category = "pressure-cooker"

    db.session.commit()

    
    if Product.query.count() == 0:
        db.session.add_all([

            
            Product(name="Steel Plate Classic", price=200, description="Classic plate", image="plate1.jpg", category="plate"),
            Product(name="Steel Plate Designer", price=250, description="Designer plate", image="plate2.jpg", category="plate"),
            Product(name="Steel Plate Heavy", price=300, description="Heavy plate", image="plate3.jpg", category="plate"),

            
            Product(name="Steel Glass Small", price=100, description="Small glass", image="glass1.jpg", category="glass"),
            Product(name="Steel Glass Medium", price=120, description="Medium glass", image="glass2.jpg", category="glass"),
            Product(name="Steel Glass Large", price=150, description="Large glass", image="glass3.jpg", category="glass"),

            
            Product(name="Steel Bowl Small", price=120, description="Small bowl", image="bowl1.jpg", category="bowl"),
            Product(name="Steel Bowl Medium", price=150, description="Medium bowl", image="bowl2.jpg", category="bowl"),
            Product(name="Steel Bowl Large", price=180, description="Large bowl", image="bowl3.jpg", category="bowl"),

            
            Product(name="Pressure Cooker 2L", price=1200, description="2 litre cooker", image="cooker1.jpg", category="pressure-cooker"),
            Product(name="Pressure Cooker 3L", price=1500, description="3 litre cooker", image="cooker2.jpg", category="pressure-cooker"),

            
            Product(name="Spoon Set 6pc", price=250, description="6 pieces", image="spoon1.jpg", category="spoon-set"),
            Product(name="Spoon Set 12pc", price=400, description="12 pieces", image="spoon2.jpg", category="spoon-set"),

            
            Product(name="Bottle 500ml", price=250, description="Small bottle", image="bottle1.jpg", category="bottle"),
            Product(name="Bottle 1L", price=300, description="Large bottle", image="bottle2.jpg", category="bottle"),

            
            Product(name="Lunch Box 2 Layer", price=400, description="2 layer box", image="tiffin1.jpg", category="lunch-box"),
            Product(name="Lunch Box 3 Layer", price=500, description="3 layer box", image="tiffin2.jpg", category="lunch-box"),

            
            Product(name="Kadai Small", price=700, description="Small kadai", image="kadai1.jpg", category="kadai"),
            Product(name="Kadai Large", price=900, description="Large kadai", image="kadai2.jpg", category="kadai"),

            
            Product(name="Frying Pan Small", price=600, description="Small pan", image="pan1.jpg", category="frying-pan"),
            Product(name="Frying Pan Large", price=800, description="Large pan", image="pan2.jpg", category="frying-pan"),

        ])

        db.session.commit()


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/products')
def products():
    search = request.args.get('search')
    if search:
        items = Product.query.filter(Product.name.contains(search)).all()
    else:
        items = Product.query.all()
    return render_template('products.html', products=items)


@app.route('/product/<int:id>')
def product_detail(id):
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product)



    return render_template('cart.html', items=cart_items, total=total)

@app.route('/increase/<int:id>')
def increase(id):
    cart = session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] += 1

    session['cart'] = cart
    return redirect(url_for('cart'))


@app.route('/decrease/<int:id>')
def decrease(id):
    cart = session.get('cart', {})

    if str(id) in cart:
        cart[str(id)] -= 1

        if cart[str(id)] <= 0:
            del cart[str(id)]

    session['cart'] = cart
    return redirect(url_for('cart'))


@app.route('/add_to_cart/<int:id>')
def add_to_cart(id):
    if 'user_id' not in session:
        flash("Please login first!", "warning")
        return redirect('/login')
    
    cart = session.get('cart', {})
    
    if str(id) in cart:
        cart[str(id)] += 1
    else:
        cart[str(id)] = 1

        session['cart'] = cart
        session.modified = True

    return redirect('/cart')    

@app.route('/reset_cart')
def reset_cart():
    session.pop('cart', None)
    return "Cart Reset Done"


@app.route('/cart')
def cart():

    cart = session.get('cart', {})

   
    if isinstance(cart, list):
        new_cart = {}
        for pid in cart:
            pid = str(pid)
            if pid in new_cart:
                new_cart[pid] += 1
            else:
                new_cart[pid] = 1

        session['cart'] = new_cart
        session.modified = True
        cart = new_cart

    cart_items = []
    total = 0

    for pid, qty in cart.items():
        product = Product.query.get(int(pid))
        if product:
            subtotal = product.price * qty
            total += subtotal

            cart_items.append({
                'product': product,
                'qty': qty,
                'subtotal': subtotal
            })

    return render_template('cart.html', items=cart_items, total=total)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == "POST":
        name = request.form['name']
        contact_no = request.form['contact_no']
        message = request.form['message']

        if not name or not message:
            flash("Please fill all fields ❗", "danger")
        else:
         flash("Message sent successfully!", "success")  # ✅ only on POST
        return redirect('/contact')  # ✅ important

    return render_template('contact.html')
    return render_template('contact.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "123":
            session['admin'] = True
            return redirect('/admin_dashboard')
        else:
            flash("Invalid username or password ❌", "danger") 

    return render_template('admin_login.html')


@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect('/admin')

    products = Product.query.all()
    orders = Order.query.all()
    users = User.query.all()  
    messages = Contact.query.all()
    return render_template('admin_dashboard.html', products=products, messages=messages, orders=orders, users=users)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
     if not session.get('admin'):
        return redirect('/admin')
     if request.method == "POST":
        name = request.form['name']
        price = request.form['price']
        desc = request.form['description']

        new_product = Product(name=name, price=price, description=desc, image="default.jpg")
        db.session.add(new_product)
        db.session.commit()

        return redirect('/admin_dashboard')

     return render_template('add_product.html')


@app.route('/delete/<int:id>')
def delete(id):
    if not session.get('admin'):
        return redirect('/admin')

    product = Product.query.get(id)
    db.session.delete(product)
    db.session.commit()
    return redirect('/admin_dashboard')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            flash("Login Successful!", "success")
            return redirect('/')
        else:
            flash("Invalid username or password", "danger")

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']

        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()

        flash("Registration Successful! Please login.", "success")
        return redirect('/login')

    return render_template('register.html')

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin', None)  
    return redirect('/admin') 

@app.route('/category/<string:cat>')
def category(cat):
    products = Product.query.filter_by(category=cat).all()
    return render_template('products.html', products=products)


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
     if 'user_id' not in session:
        return redirect('/login')

     cart = session.get('cart', {})

     if not cart:
        return redirect('/cart')

     if request.method == "POST":
        name = request.form['name']
        address = request.form['address']

        
        product_list = []

        for pid, qty in cart.items():
            product = Product.query.get(int(pid))
            if product:
                product_list.append(f"{product.name} x {qty}")

        
        new_order = Order(
            customer_name=name,
            address=address,
            items=", ".join(product_list),
            user_id=session['user_id']   
        )

        db.session.add(new_order)
        db.session.commit()

        
        session.pop('cart', None)

        return render_template('order_success.html', name=name)

     return render_template('checkout.html')

@app.route('/orders')
def orders():

    if 'user_id' not in session:
        return redirect('/login')

    user_orders = Order.query.filter_by(user_id=session['user_id'],
                                          is_hidden=False   # 👈 important
    ).all()


    return render_template('orders.html', orders=user_orders)

@app.route('/admin_clear_orders')
def clear_orders():

    if not session.get('admin'):
        return redirect('/admin')
    Order.query.delete()
    db.session.commit()
    return redirect('/admin_dashboard')

@app.route('/user_clear_orders')
def user_clear_orders():

    if 'user_id' not in session:
        return redirect('/login')

    Order.query.filter_by(user_id=session['user_id']).delete()
    db.session.commit()

    return redirect('/orders')


if __name__ == "__main__":
    app.run(debug=True)