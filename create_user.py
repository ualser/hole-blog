"""Create a new admin user able to view the /reports endpoint."""
from getpass import getpass
import sys, md5

from flask import current_app
from app import app
from app.models import User, db

def main():
    """Main entry point for script."""
    with app.app_context():
        db.metadata.create_all(db.engine)
        if User.query.all():
            print 'A user already exists! Create another? (y/n):',
            create = raw_input()
            if create == 'n':
                return

        print 'Enter email address: ',
        email = raw_input()
        password = getpass()
        assert password == getpass('Password (again):')
	print password
	m = md5.new()
	m.update(password)
        print 'Enter nickname: '
	nickname = raw_input()
	print 'Is admin y/n? '
	answer = raw_input()
	if answer == 'y': user = User(nickname=nickname, email=email, password=m.hexdigest(), is_admin=True)
	else: user = User(nickname=nickname, email=email, password=m.hexdigest()) 
	print m.hexdigest()
	db.session.add(user)
        db.session.commit()
        print 'User added.'



if __name__ == '__main__':
    sys.exit(main())

