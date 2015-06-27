import datetime
from app import db, models

u = models.User(nickname='john', email='john@email.com')
db.session.add(u)
db.session.commit()
u = models.User(nickname='susan', email='susan@email.com')
db.session.add(u)
db.session.commit()
u = models.User.query.get(1)
p = models.Post(body='my first post!', timestamp=datetime.datetime.utcnow(), author=u)
db.session.add(p)
db.session.commit()
