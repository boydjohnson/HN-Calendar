# flask calendar event posting site
from flask import Flask, render_template
from flask.ext.triangle import Triangle
import calendar
app = Flask(__name__,instance_path='C:/Documents and Settings/Owner/My Documents/Downloads/RealPython Homework/flask-hn')
Triangle(app)

months=list(calendar.month_name)
months_iter=8

#Urls
@app.route('/')
def homepage():
	return render_template('main.html',months=months,months_iter=months_iter)


if __name__ == '__main__':
	app.run(debug=True)