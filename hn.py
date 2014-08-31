# flask calendar event posting site
from flask import Flask, redirect, url_for, render_template, request, jsonify, flash
import datetime
from calendar import Calendar
from wtforms import Form, TextField, validators, DateField
from flask.ext.sqlalchemy import SQLAlchemy
from re import compile
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI


app = Flask(__name__,instance_path='C:/Documents and Settings/Owner/My Documents/Downloads/RealPython Homework/flask-hn', instance_relative_config=True)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db= SQLAlchemy(app)
regex = compile('#')

	
class poster(Form):
	title = TextField('title of event',[validators.Length(min=2, max=60)])
	content = TextField('What is the event about?',[validators.Length(min=6,max=500)])
	hash_tag = TextField('hash tag',[validators.Regexp(regex)])
	date = DateField('Date of event',[validators.Required()])

# Model
class post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	post_title = db.Column(db.String(100))
	post_content = db.Column(db.String(500))
	post_date = db.Column(db.DateTime())
	post_hash = db.Column(db.String(100))
	post_user = db.Column(db.String(60))
	
	def __init__(self, title, content, hash, date):
		self.post_title = title
		self.post_content = content
		self.post_hash = hash
		self.post_date = date
		
	def __repr__(self):
		return self.post_title
	

	# Get dates and calendar of dates for Homepage
now = datetime.datetime.now()
current_month=now.month
current_year=now.year

def get_days_for_dates(year):
	year_dates= Calendar().yeardayscalendar(year)
	arr=[];
	for quarter in year_dates:
		for month in quarter:
			for week in month:
				for date in week:
					arr.append(date)
	return arr

	
year_calendar = get_days_for_dates(current_year)



#Urls
@app.route('/')
def homepage():
	q = post.query.with_entities(post.post_title, post.post_content, post.post_hash, post.post_date, post.id).all()
	return render_template('main.html',current_month=current_month,current_year=current_year,year_calendar=year_calendar,posts=q)

@app.route('/post',methods=['GET', 'POST'])
def post_form():
	form = poster(request.form)
	if request.method == 'POST' and form.validate():
		p = post(form.title.data,form.content.data,form.hash_tag.data,form.date.data)
		db.session.add(p)
		db.session.commit()
		flash("Thanks for posting your event!")
		return redirect(url_for('homepage'))
	return render_template('post.html', form=form)

@app.route('/event/<int:id_number>',methods=['GET'])
def specific_event(id_number):
	q = post.query.with_entities(post.post_title,post.post_content,post.post_hash,post.post_date).filter(post.id==id_number).first()
	return render_template('spec_event.html', posts=q)
	
# route for AJAX request
@app.route('/day-lookup/', methods=['GET'])
def day_lookup():
	year=request.args.get('year',None)
	
	return jsonify(dates=get_days_for_dates(int(year)))
	

if __name__ == '__main__':
	app.run(debug=True)