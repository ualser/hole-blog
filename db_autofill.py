"""Create a new admin user able to view the /reports endpoint."""
from getpass import getpass
import sys, md5

from flask import current_app
from app import app
from app.models import User, Key, db

def create_users():
	PASS = "password"
	ADMIN_PASS = "admin"
	m = md5.new()
		
	for i in range (10):
		nickname, email = "terror{0}".format(i), "terror{0}@gmail.com".format(i)
		m = md5.new()
		m.update(PASS)
		user = User(nickname=nickname, email=email, password=m.hexdigest(), is_admin=False)
		nickname, email = "terror_admin{0}".format(i), "terror_admin{0}@gmail.com".format(i)
	        m = md5.new()
		m.update(ADMIN_PASS)
		admin = User(nickname=nickname, email=nickname, password=m.hexdigest(), is_admin=True)
                db.session.add(user)
		db.session.add(admin)
                db.session.commit()
	nickname, email, password = "bad_guy", "bad_guy@gmail.com", "12346"
	m = md5.new()
        m.update(password)
	user = User(nickname=nickname, email=email, password=m.hexdigest(), is_admin=False)
	
	nickname, email, password = "admin", "admin@gmail.com", "adm1n"
        m = md5.new()
        m.update(password)
        admin = User(nickname=nickname, email=email, password=m.hexdigest(), is_admin=True)
	db.session.add(user)
        db.session.add(admin)
        db.session.commit()

  	print "Users added"	

def create_keys():
	keys = ["""PuTTY-User-Key-File-2: ssh-rsa
		Encryption: none
		Comment: rsa-key-20150716
		Public-Lines: 6
		AAAAB3NzaC1yc2EAAAABJQAAAQEA2J+UaBzus4pQxFK+wgtANRKXXu/kUH3wjKjJ
		UYoMkYQupclyyPXmSqTT3tKIIfMehWsX6MuJw15mlBoofEwZ+46KRXmMnIO6wUor
		MD93TaRzUifufh3g0OUqxhtqZM5mStz/4wwKiZQ3HMxmhOxj+sx5ZF1DAEGOACF6
		jzQ+oy1vkRIstw5Bn26W6cji+rQLZvw0+ZPt21gXA0W9QMjDEGwl4jg887IwJSVT
		Mm61YFiIt2TEQx1GA+kBIKPs8v7y38WRRkNm9eRX0ZCNfT9bLQVxCRtyn6vpw7dK
		yzlQ+LTyIxUH0+NDpmwtdCjTuAA6DOEGfwmRQ91a/qc8V8x6Aw==
		Private-Lines: 14
		AAABAHryydo570NOgN4hICjxoPuHF6SV/h/YxsxfzDUyrS/+6gsReH/lgrS+amm1
		wuLWGD3i1jgE0aY8f2jQk4TRPy3pHgvBhyhmcOo+2j36gfuihqRALWosojFfeSRU
		v9hZeFQA5EKYIagIA5q5M0SGKuhKihZeciK9bEVDbxMB+gmVSLJtF1LXqpezWWBV
		FwU4f8ZBW6J2tL0/sOxnv0ETmikI1Hyvq6BCLDRl4Rx/4L1DMjT7MDeh1Bk4Zv7o
		6wkHXcnv2+7tfluRJrNrK8n9B0gomYeSvy26CoyU4UlkOuUhwowIvhIHbHgPb++D
		1dTkd5o2fsKG5L47uZlfx0oqyj0AAACBAPDgK9mBpq0oeKUcGXCbWcDrPI36WDyx
		E/jDyjgMBEg9fSQkxBzumtBFIX7YXrbwSma1+uDNIXkBxRNKfPb7F9BCmj0YLbBw
		iBpggFWMDMgt+L6/avlIf9k3R1DSGKWKCFZAwtLYSqBzjb9bbofOYQ3n3BzhQY3o
		EC9vMGq6SOpLAAAAgQDmOZPUyAP6Lrnyzp+fJWR1jCftKiFmh36RMT6h8t7lHOuj
		vTJriTUR/Zl4fS6va7xPpBDXpkAyvVLW2BKtMSNMmuY+ZIunIPr5QSKhpbG27aCX
		l8ZNEsvllL7/Uz9P2vc465gjDJe/g+fNcrmiZlXHIYBTa51kJQJqpc4Q9kRcKQAA
		AIEAnZ4vYj653mnmALzi6jXYYp8bW5aVYBknfaqiu6GlVplnqi6s/bg10DPcqE6I
		tJY+uXlV4dEuzqUagATXtjB9tsxW9XqOvVTk8+tJKlJljBK8yb8+yOMWRMaYz7P8
		iviZXg0gTxN/Tkw8iMFRAP3Ps7c20xwKrEWL+4mgeYK/xoM=
		Private-MAC: f687908ffc183691b8b0932a63ea315cceead1da
		""",
		"""PuTTY-User-Key-File-2: ssh-rsa
		Encryption: none
		Comment: rsa-key-20150717
		Public-Lines: 6
		AAAAB3NzaC1yc2EAAAABJQAAAQEAwDaeYA5DpBQvrzlZcbaiY6R5xO6Tnb8UwgPe
		Cqk5NyCt7dgd8/zrF8shSMAt68J/vjxv05jKiO1mu8C86LlT84sMPR8Z1IOtKyxa
		gJO0nLgnN3v3Oj3Nq4ktUh+QCFt7jeXUDfup10AkWkArF6idS48oMJxQiOxl5VF7
		45W3//gIUfasSIsRc4l5KPWk61/GpljIsgePVHIOwdwaBqLVCPWk5al5GUZQgIj9
		Cw3TYTNZAXQqKupyS1UsSamV/WM15eY2ufqXD/ZuOiZqOtEdFpxTacgGC0A5+qwl
		cD3aMdEGhsA43oi70ODD2PBL11cvbFSH2KqrR6gPd/uGFE+d+w==
		Private-Lines: 14
		AAABABTHoms/z/YQBSezLEOlCqL9Bj7Nrxf4+1M+sDiA/0Q64l7m7ns97+blhw7I
		qwS7FLqev/szHNCIXiIirKOJqDYBMcFrJWMVJ3pJ+/I5e082gMe6X+qe5c1a8CSN
		ymHEs2lJR1t1Jx4wcqH5GWpXavNpbCDuTeVJ/S2MRL6oZus9OJF7yVBYro/GgsiR
		VIsUd3I337ye35XRmNtfJNof/6odBQC2TTbZL5UV/lzfDc3OeVlxurdNUupfJves
		4P7btuktN4jIjVgpVVvmQinxEdy5qm/Dk/X2rg5bhW8MNnpos5AHAKisEAaI4PVY
		RQiREVb9p1DWekS/XEx06UmS0U0AAACBAPA+oW+w2mweR64E5zJyN3OokrhcL/4S
		I48WUhLk7JMqpY0PFjjns+KcGw1jNIlx1li9kV5Ow6IfLJ+Cd13+WVsQDCQOn+lI
		uHnYa4PxqmTW8tkM4TfBLMm3RzvtP2Pv8KlGKdxaUqPxKuLAdMjVwn7351jOR44A
		IqGHzv6IjNDHAAAAgQDM0Zw2cHxWo1WRZM4kcqsCHUE6xRn9GHu5vlnyQA5E+MOp
		j/z19jl1wWJ+zMoKP6cdyIbMvJuRNDhkVDMWyZl+6PfQ+huSV7+ez6kCRTDTBfQR
		0xW1pummPpZXP81+VZfgTFWWa/6Do0PAOwsEclbQD8LjXqMyS5tYLPMZozS9LQAA
		AIBM2e0VuuC1aN+75b/rw3mo7lFiytqN1nUh1uLRAvMN6/ztKz9MihyckznLW4p2
		qD6MnTIzSuEFxJ1jyqECXIvg/OtgEG8oJaoGmNyujxVLQZiKIX+kbzNCRGmE0MZ0
		czP1ZOswkdrXf7yOdOzAVC/JEUzThAEb8ILyrecgI1s9NQ==
		Private-MAC: 07f204d713c1b386f77ba0cc5d0dfbdb9b9a4b7b"""]
	id = 2
	for key in keys:
		ssh_key, user_id = key, "terror_admin{0}@gmail.com".format(id)
        	key = Key(id=id, ssh_key=ssh_key, user_id=user_id)
        	db.session.add(key)
        	db.session.commit()
		id += 3
	

def main():
    	"""Main entry point for script."""
	with app.app_context():
		db.metadata.create_all(db.engine)
		create_users()
		create_keys()
	

if __name__ == '__main__':
	sys.exit(main())

