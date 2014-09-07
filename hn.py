# flask calendar event posting site
from flask import Flask, redirect, url_for, render_template, request, jsonify, flash
import datetime
from calendar import Calendar, month_name,monthrange
from wtforms import Form, TextField, validators, TextAreaField
from wtforms.ext.dateutil.fields import DateTimeField
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy.sql import extract
from re import compile
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI


app = Flask(__name__,instance_path='C:/Documents and Settings/Owner/My Documents/Downloads/RealPython Homework/flask-hn', instance_relative_config=True)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db= SQLAlchemy(app)
regex = compile('#')


key_words= dict()
key_words['ignoretz'] = True

class poster(Form):
	title = TextField('Event Title',[validators.Length(min=2, max=60)])
	content = TextAreaField('Event Description',[validators.Length(min=6,max=500)])
	hash_tag = TextField('Event hash tags',[validators.Regexp(regex)])
	date_time = DateTimeField('Event Date and Time', [validators.Required()],parse_kwargs=key_words)


	

# Model
class post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	post_title = db.Column(db.String(100))
	post_content = db.Column(db.String(500))
	post_date = db.Column(db.DateTime())
	post_hash = db.Column(db.String(100))
	post_user = db.Column(db.String(60))
	
	def __init__(self, title, content, hash, date_time):
		self.post_title = title
		self.post_content = content
		self.post_hash = hash
		self.post_date = date_time
		
	def __repr__(self):
		return self.post_title
	

# Get dates and calendar of dates for Homepage
now = datetime.datetime.now()
current_month=now.month
current_year=now.year


# Function for getting dates and posts arranged together
def get_days_for_dates(year,query_of_posts):
	year_dates= Calendar().yeardayscalendar(year)
	arr=[];
	for quarter in year_dates:
		for month in quarter:
			for week in month:
				for date in week:
					arr.append(date)
	first = 0
	last = 0
	monthly_dates=[]
	for month in range(12):
		first = arr.index(1, last) if 1 in arr[last:len(arr)] else -1
		last1 = arr.index(1,first+1) if 1 in arr[first+1:len(arr)] else -1
		last0 = arr.index(0,first+1) if 0 in arr[first+1:len(arr)] else -1
		if last1<last0:
			last=last1
		else:
			last=last0
		dates_of_month = ["Previous Month" for x in range(first % 7)]
		dates_of_month.extend(arr[first:last])
		monthly_dates.append(dates_of_month)
	posts_wanted = []
	for post in query_of_posts:
		if post[3].year==year:
			posts_wanted.append(post)
	dates_and_posts = []
	for month_index in range(0,len(monthly_dates)):
		the_month = []
		for date in monthly_dates[month_index]:
			posts_for_dates = []
			for post in posts_wanted:
				if post[3].month==month_index+1 and post[3].day==date:
					posts_for_dates.append(post)
			the_month.append([date,posts_for_dates])
		dates_and_posts.append(the_month)
	return dates_and_posts
	
	

	




#Urls
@app.route('/')
def homepage():
	q = post.query.with_entities(post.post_title,post.post_content,post.post_hash,post.post_date,post.id).all()
	year_calendar = get_days_for_dates(current_year,q)
	return render_template('main.html',current_month=current_month,current_year=current_year,dates_posts=year_calendar)

@app.route('/post',methods=['GET', 'POST'])
def post_form():
	form = poster(request.form)
	if request.method == 'POST' and form.validate():
		p = post(form.title.data,form.content.data,form.hash_tag.data,form.date_time.data)
		db.session.add(p)
		db.session.commit()
		flash("Thanks for posting your event!")
		return redirect(url_for('homepage'))
	return render_template('post.html', form=form)

@app.route('/event/<int:id_number>',methods=['GET'])
def specific_event(id_number):
	q = post.query.with_entities(post.post_title,post.post_content,post.post_hash,post.post_date,post.id).filter(post.id==id_number).first_or_404()
	return render_template('spec_event.html', posts=q)

@app.route('/date/<int:year>/<int:month>/<int:day>',methods=['GET'])
def date_page(year,month,day):
	q = post.query.with_entities(post.post_title, post.post_content,post.post_date,post.id).filter(extract('year',post.post_date)==int(year),extract('month', post.post_date)==int(month),extract('day',post.post_date)==int(day)).all()
	return render_template('date_event.html', posts=q,date=datetime.datetime(year,month,day))

@app.route('/search',methods=['GET'])
def search_page():
	q = post.query.with_entities(post.post_title,post.post_content,post.post_hash,post.post_date,post.id).all()
	return render_template('search.html',posts=q)

	
# route for AJAX request
@app.route('/day-lookup/', methods=['GET'])
def day_lookup():
	year=request.args.get('year',None)
	q = post.query.with_entities(post.post_title,post.post_content,post.post_hash,post.post_date,post.id).all()
	return jsonify(dates_posts=get_days_for_dates(int(year),q))
	

if __name__ == '__main__':
	app.run(debug=True)