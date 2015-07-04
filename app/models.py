from app import db

class User(db.Model):
    nickname = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), primary_key=True, index=True, unique=True)
    password = db.Column(db.String(15))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    authenticated = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<User %r>' % (self.email)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.email

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.email'))

    def __repr__(self):
        return '<Post %r>' % (self.body)
