# flask calendar event posting site
from flask import Flask, redirect, url_for, render_template, request, jsonify, flash
import datetime
from calendar import Calendar
from wtforms import Form, TextField, validators, DateField
from hnModels import post, db
from re import compile
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI


app = Flask(__name__,instance_path='C:/Documents and Settings/Owner/My Documents/Downloads/RealPython Homework/flask-hn', instance_relative_config=True)

app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI

regex = compile('#')
db.init_app(app)

class poster(Form):
	title = TextField('title of event',[validators.Length(min=2, max=60)])
	content = TextField('What is the event about?',[validators.Length(min=6,max=500)])
	hash_tag = TextField('hash tag',[validators.Regexp(regex)])
	date = DateField('Date of event',[validators.Required()])

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
	return render_template('main.html',current_month=current_month,current_year=current_year,year_calendar=year_calendar)

@app.route('/post',methods=['GET', 'POST'])
def post_form():
	form = poster(request.form)
	if request.method == 'POST' and form.validate():
		p = post(form.title.data,form.content.data,form.hash_tag.data,form.date.data)
		db.session.add(p)
		flash("Thanks for posting your event!")
		return redirect(url_for('homepage'))
	return render_template('post.html', form=form)

# route for AJAX request
@app.route('/day-lookup/', methods=['GET'])
def day_lookup():
	year=request.args.get('year',None)
	
	return jsonify(dates=get_days_for_dates(int(year)))
	

if __name__ == '__main__':
	app.run(debug=True)