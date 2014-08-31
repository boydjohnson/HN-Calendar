# HN models
from flask.ext.sqlalchemy import SQLAlchemy

db =SQLAlchemy()

class post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	post_title = db.Column(db.String(100))
	post_content = db.Column(db.String(500))
	post_date = db.Column(db.DateTime)
	post_hash = db.Column(db.String(100))
	post_user = db.Column(db.String(60))
	
	def __init__(self, title, content, hash, date):
		self.post_title = title
		self.post_content = content
		self.post_hash = hash
		self.post_date = date
		