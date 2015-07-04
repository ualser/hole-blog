from flask import render_template, request, redirect, url_for
from app import app, db, models
import datetime, md5
from flask.ext.login import LoginManager, UserMixin, login_required, login_user
from flask.ext.sqlalchemy import SQLAlchemy
from .forms import LoginForm

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'Miguel'}  # fake user
    posts = [  # fake array of posts
        { 
            'author': {'nickname': 'John'}, 
            'body': 'Beautiful day in Portland!' 
        },
        { 
            'author': {'nickname': 'Susan'}, 
            'body': 'The Avengers movie was so cool!' 
        }
    ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)

@app.route('/add_post', methods=['POST'])
def add_post():
	user = request.form['user']
	p = request.form['post']
	u = models.User.query.get(user)
	p = models.Post(body=p, timestamp=datetime.datetime.utcnow(), author=u)
	db.session.add(p)
	db.session.commit()
	posts = u.posts.all()
	return render_template("form.html",
                           title='Home',
                           user_id=user,
                           user=u,
                           posts=posts)

@app.route('/view_posts')
@login_required
def view_posts():
	email = request.args.get('email')
	e = models.User.query.get(email)
	posts = e.posts.all()
	return render_template("form.html",
                           title='Home',
			   user_id=email,
                           user=e,
                           posts=posts)

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return models.User.query.get(user_id)

@app.route('/reports')
@login_required
def reports():
    """Run and display various analytics reports."""
    products = Product.query.all()
    purchases = Purchase.query.all()
    purchases_by_day = dict()
    for purchase in purchases:
        purchase_date = purchase.sold_at.date().strftime('%m-%d')
        if purchase_date not in purchases_by_day:
            purchases_by_day[purchase_date] = {'units': 0, 'sales': 0.0}
        purchases_by_day[purchase_date]['units'] += 1
        purchases_by_day[purchase_date]['sales'] += purchase.product.price
    purchase_days = sorted(purchases_by_day.keys())
    units = len(purchases)
    total_sales = sum([p.product.price for p in purchases])

    return render_template(
            'reports.html',
            products=products,
            purchase_days=purchase_days,
            purchases=purchases,
            purchases_by_day=purchases_by_day,
            units=units,
            total_sales=total_sales)

@app.route("/login", methods=["GET", "POST"])
def login():
    """For GET requests, display the login form. For POSTS, login the current user
    by processing the form."""
    form = LoginForm()
    print "in login", form.validate_on_submit()
    if form.validate_on_submit():
        print "In 1 if"
	print form.email.data, "\n"
	
	user = models.User.query.get(form.email.data)
        print "\n++++\n"
	if user:
           print "in second if" 
	   m=md5.new()
	   m.update(form.password.data)	
	   print form.password.data
	   print str(buffer(m.digest())), str(user.password)
	   if user.password == buffer(m.digest()):
                print "In if bitch!"
		user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
                return redirect("http://127.0.0.1:5000/view_posts?email="+form.email.data, 302)
    return render_template("login.html", form=form)

@app.route("/logout", methods=["GET"])
@login_required
def logout():
    """Logout the current user."""
    user = current_user
    user.authenticated = False
    db.session.add(user)
    db.session.commit()
    logout_user()
    return render_template("logout.html")
 
