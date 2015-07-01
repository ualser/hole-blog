from flask import render_template, request
from app import app, db, models
import datetime

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

@app.route('/add_user')
def add_user():
	u = models.User(nickname='sbres', email='sbres@email.com')
	db.session.add(u)
	db.session.commit()
	return 'user added!'

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
def view_posts():
	user = request.args.get('user')
	u = models.User.query.get(user)
	posts = u.posts.all()
	return render_template("form.html",
                           title='Home',
			   user_id=user,
                           user=u,
                           posts=posts)

 
