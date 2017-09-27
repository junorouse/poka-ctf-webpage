from db import init_db
from os import remove
from time import sleep

try:
	remove("db.sqlite3")
except:
	pass

init_db()

from db import db_session
from models import *

postech_password = 'postech5461'
kaist_password = 'kaist1401'

postech = User('postech', postech_password)
kaist = User('kaist', kaist_password)
admin = User('admin', '**blind**')
score = 89

chall0 = Challenge(0, 'prob0', 'prob0.png', '''
		desc
''', score, 'flag{this-is-flag}')

db_session.add(postech)
db_session.add(kaist)
db_session.add(admin)


db_session.add(chall0)
# you have to make 16 challs
'''
db_session.add(chall1)
db_session.add(chall2)
db_session.add(chall3)
db_session.add(chall4)
db_session.add(chall5)
db_session.add(chall6)
db_session.add(chall7)
db_session.add(chall8)
db_session.add(chall9)
db_session.add(chall10)
db_session.add(chall11)
db_session.add(chall12)
db_session.add(chall13)
db_session.add(chall14)
db_session.add(chall15)
'''

db_session.commit()

