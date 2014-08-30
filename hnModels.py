# HN models
from config import db

class post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	post_title = db.Column(db.String(240))
	post_content = db.Column(db.String(400))
	post_date = db.Column(db.DateTime)
	post_user = db.Column(db.String(60))
	
