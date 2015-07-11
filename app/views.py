from flask import render_template, request, redirect, url_for
from app import app, db, models
import datetime, md5
from flask.ext.login import LoginManager, UserMixin, login_required, login_user, current_user
from flask.ext.sqlalchemy import SQLAlchemy
from .forms import LoginForm

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/add_post', methods=['POST']) #missing function level control vulnerability
def add_post():
	user = request.form['user']
	p = request.form['post']
	u = models.User.query.get(user)
	p = models.Post(body=p, timestamp=datetime.datetime.utcnow(), author=u)
	db.session.add(p)
	db.session.commit()
	posts = u.posts.all()
	return redirect("http://192.168.72.133:5000/view_posts?email=" + user, 302) 

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
                           posts=posts,
			   admin=is_admin(current_user.get_id()))

@app.route('/admin', methods=['GET'])
@login_required
def admin():
	if is_admin(current_user.get_id()):
		return render_template("secret_admin_page.html")	
	else: return render_template("admin_access_required.html") 

def is_admin(email):
	u = models.User.query.get(email)
	return u.is_admin

@app.route('/change_password')
@login_required
def change_password():
	new_pass = request.args.get('new_pass')
	print "new pass is ", new_pass
	user_id = current_user.get_id()
	m = md5.new()
        m.update(new_pass)
	user = models.User.query.get(user_id)
	user.password = buffer(m.hexdigest())
	db.session.commit() 
	return 'OK'
	

@login_manager.user_loader
def user_loader(user_id):
    """Given *user_id*, return the associated User object.

    :param unicode user_id: user_id (email) user to retrieve
    """
    return models.User.query.get(user_id)

@app.route("/")
@app.route("/index")
@app.route("/login", methods=["GET", "POST"])
def login():
    """For GET requests, display the login form. For POSTS, login the current user
    by processing the form."""
    if current_user.is_authenticated():
	redirect_url = request.args.get('redirect_url')
    	if redirect_url:
        	return redirect('http://' + redirect_url,  302)
	else: return redirect("http://192.168.72.133:5000/view_posts?email=" + current_user.get_id(), 302)
    form = LoginForm()
    if form.validate_on_submit():
	user = models.User.query.get(form.email.data)
	if user:
	   m=md5.new()
	   m.update(form.password.data)	
	   if user.password == buffer(m.hexdigest()):
		user.authenticated = True
                db.session.add(user)
                db.session.commit()
                login_user(user, remember=True)
		print "now will be redirect!"
		return redirect("http://192.168.72.133:5000/view_posts?email=" + current_user.get_id(), 302)
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

@app.route("/search", methods=["POST"])
def search():
    search_results = [] 
    search_string = request.form["search"]
    posts = []
    q = db.engine.execute("SELECT user_id, body FROM post WHERE body LIKE {0}".format(search_string))
    for row in q:
    	posts.append(row)
    nicknames = get_nicknames(posts)
    for i in range(len(nicknames)):
	print i, posts[i]
	search_results.append([nicknames[i], posts[i][1]])
    """
    for oin range(len(nicknames)):
    	search_results[nicknames[i]] = q[i][1]
    """
    print search_results
    return render_template("search_results.html", search_results = search_results)

def get_nicknames(posts):
    nicknames = []
    query_result = ''
    for row in posts:
	query_result = db.engine.execute("SELECT nickname FROM user WHERE email=?", [row[0]])
   	for item in query_result: nicknames.append(item[0])
    return nicknames

@login_manager.unauthorized_handler
def unauthorized():
    # do stuff
    return render_template("unauth.html")

@app.context_processor
def get_all_user_ids():
    def get_ids():
	print 'i am in here'
	ids = []
	users = models.User.query.order_by(models.User.email)
	for user in users: 
		ids.append([user.email, user.nickname])	
	return ids  
    return dict(get_all_user_ids=get_ids)
