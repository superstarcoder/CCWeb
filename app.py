#taken help from https://pythonspot.com/flask-web-forms/

from flask import Flask, render_template, flash, request, send_from_directory, redirect, url_for
from wtforms import Form, TextField, TextAreaField, validators, StringField, SubmitField
import os

# App config.
DEBUG = True
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

class ReusableForm(Form):
    title = TextField('title:', validators=[validators.DataRequired()])

    time1 = TextField('time1:', validators=[validators.DataRequired()])
    time2 = TextField('time2:', validators=[validators.DataRequired()])

    duedate1 = TextField('duedate1:', validators=[validators.DataRequired(), validators.Length(min=3, max=35)])
    duedate2 = TextField('duedate2:', validators=[validators.DataRequired(), validators.Length(min=3, max=35)])
    assignment1 = TextField('assignment1:', validators=[validators.DataRequired()])
    assignment2 = TextField('assignment2:', validators=[validators.DataRequired()])
    paste = TextField('paste:', validators=[validators.DataRequired()])
    
    @app.route("/", methods=['GET', 'POST'])
    def hello():
        form = ReusableForm(request.form)
    
        print(form.errors)
        if request.method == 'POST':
            title=request.form['title']
            duedate1=request.form['duedate1']
            duedate2=request.form['duedate2']
            time1=request.form['time1']
            time2=request.form['time2']
            assignment1=request.form['assignment1']
            assignment2=request.form['assignment2']
            paste=request.form['paste']

            print("---------------------------------")
            print("title:",title)
            print("duedate1:",duedate1)
            print("duedate2:",duedate2)
            print("time1:",time1)
            print("time2:",time2)
            print("assignment1:",assignment1)
            print("assignment2:",assignment2)
            print("pasted: ",paste)
            print("---------------------------------")
            import backend
            backend.run(title, duedate1, duedate2, time1, time2, assignment1, assignment2, paste)
            #return render_template('table.html', form=form)
            return redirect(url_for('table'))
    
        if form.validate():
            flash('Thanks for registration ' + title)
        else:
            flash('Error: All the form fields are required. ')
    
        return render_template('index.html', form=form)
    @app.route("/help/", methods=['POST'])
    def help():
        form = ReusableForm(request.form)
    
        return render_template('help.html', form=form)
    @app.route('/css/<path:path>')
    def css(path):
        return send_from_directory('templates/css',path)

    @app.route('/vendor/<path:path>')
    def vendor(path):
        return send_from_directory('templates/vendor',path)

    @app.route('/js/<path:path>')
    def js(path):
        return send_from_directory('templates/js',path)

    @app.route('/images/<path:path>')
    def images(path):
        return send_from_directory('templates/images',path)

    @app.route('/resources/<path:path>')
    def resources(path):
        return send_from_directory('templates/resources',path)
    
    @app.route('/table')
    def table():
        return render_template('table.html')

if __name__ == "__main__":
    app.run()
