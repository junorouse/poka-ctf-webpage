from sqlalchemy import Column, Integer, String
from db import Base
from time import time

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    password = Column(String(256))

    def __init__(self, username=None, password=None):
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r - %r>' % (self.username, self.password)


class Challenge(Base):
	__tablename__ = 'challengs'
	id = Column(Integer, primary_key=True)
	chall_id = Column(Integer, unique=True)
	chall_title = Column(String(512))
	chall_img = Column(String(256))
	chall_detail = Column(String(4096))
	chall_score = Column(Integer)
	chall_flag = Column(String(512))

	def __init__(self, chall_id, chall_title, chall_img, chall_detail, chall_score, chall_flag):
		self.chall_id = int(chall_id)
		self.chall_title = chall_title
		self.chall_img = chall_img
		self.chall_detail = chall_detail
		self.chall_score = int(chall_score)
		self.chall_flag = chall_flag

	def __repr__(self):
		return '<Challenge [%r]%r - %r>' % (self.chall_id, self.chall_title, self.chall_score)


class AuthLog(Base):
	__tablename__ = 'auth_logs'
	id = Column(Integer, primary_key=True)
	chall_id = Column(Integer)
	chall_title = Column(String(256))
	user_id = Column(Integer)
	username = Column(String(256))
	submit_flag = Column(String(512))
	submit_time = Column(Integer) # timestamp
	is_solve = Column(Integer, default=0)

	def __init__(self, chall_id, chall_title, user_id, username, submit_flag, is_solve):
		self.chall_id = int(chall_id)
		self.chall_title = chall_title
		self.user_id = int(user_id)
		self.username = username
		self.submit_flag = submit_flag
		self.submit_time = time()
		self.is_solve = is_solve

	def __repr__(self):
		return '<AuthLog [%r - %r][%r - %r]>' % (self.chall_id, self.username, self.submit_flag, self.submit_time)


class Notice(Base):
	__tablename__ = 'notice'
	id = Column(Integer, primary_key=True)
	detail = Column(String(1024))
	n_time = Column(Integer) # timestamp

	def __init__(self, detail):
		self.detail = detail
		self.n_time = time()

	def __repr__(self):
		return '<Notice [%r - %r]>' % (self.detail, self.n_time)
