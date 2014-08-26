# flask calendar event posting site
from flask import Flask, render_template
from flask.ext.triangle import Triangle
import calendar
app = Flask(__name__,instance_path='C:/Documents and Settings/Owner/My Documents/Downloads/RealPython Homework/flask-hn')
Triangle(app)

current_month=8
current_year=2014

#Urls
@app.route('/')
def homepage():
	return render_template('main.html',current_month=current_month,current_year=current_year)


if __name__ == '__main__':
	app.run(debug=True)