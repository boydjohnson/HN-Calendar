# flask calendar event posting site
from flask import Flask, redirect, url_for, render_template, request, jsonify, flash
import datetime
from calendar import Calendar, month_name,monthrange
from wtforms import Form, TextField, validators,SelectField, TextAreaField, IntegerField
from flask.ext.sqlalchemy import SQLAlchemy
from re import compile
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI


app = Flask(__name__,instance_path='C:/Documents and Settings/Owner/My Documents/Downloads/RealPython Homework/flask-hn', instance_relative_config=True)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

db= SQLAlchemy(app)
regex = compile('#')

month_choices = zip(range(1,13),month_name[1:13])

hours = ['Midnight']
hours.extend(["{:d} AM".format(num) for num in range(1,12)])
hours.append('Noon')
hours.extend(["{:d} PM".format(num) for num in range(1,12)])
hour_choices = zip(range(0,24), hours)



class poster(Form):
	title = TextField('title of event',[validators.Length(min=2, max=60)])
	content = TextAreaField('What is the event about?',[validators.Length(min=6,max=500)])
	hash_tag = TextField('hash tag',[validators.Regexp(regex)])
	year = IntegerField('Year', [validators.Length(min=4,max=4)])
	month = SelectField('Month', [validators.Required()],choices=month_choices)
	date = SelectField('Day of the Month',[validators.Required()])
	hour = SelectField('Time Hour', [validators.Required()], choices= hour_choices,default=12)
	minute = SelectField('Time Minutes',[validators.Required()], choices=zip(range(0,60),range(0,60)))
	
def edit_date(form):
	if str(form.month.data)=="None":
		date_list = []
	else:
		date_list = range(1,monthrange(int(str(form.year.data)),int(str(form.month.data)))[1])

	return zip(date_list,date_list)

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
	form.date.choices = edit_date(form)
	if request.method == 'POST' and form.validate():
		p = post(form.title.data,form.content.data,form.hash_tag.data,datetime.datetime(int(str(form.year.data)),int(str(form.month)).data,form.date.data,form.hour.data,form.minutes.data))
		db.session.add(p)
		db.session.commit()
		flash("Thanks for posting your event!")
		return redirect(url_for('homepage'))
	return render_template('post.html', form=form)

@app.route('/event/<int:id_number>',methods=['GET'])
def specific_event(id_number):
	q = post.query.with_entities(post.post_title,post.post_content,post.post_hash,post.post_date).filter(post.id==id_number).first_or_404()
	return render_template('spec_event.html', posts=q)
	
# route for AJAX request
@app.route('/day-lookup/', methods=['GET'])
def day_lookup():
	year=request.args.get('year',None)
	
	return jsonify(dates=get_days_for_dates(int(year)))
	

if __name__ == '__main__':
	app.run(debug=True)