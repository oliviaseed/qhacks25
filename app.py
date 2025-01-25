from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB connection
client = MongoClient("mongodb+srv://ethney:o2iyHC1whuSha1JX@cluster0.wq9eh.mongodb.net/")
db = client['users']
users_collection = db['user']

# Login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=50)])
    submit = SubmitField('Login')

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Save to MongoDB
        users_collection.insert_one({'username': username, 'password': password})
        flash('Login data saved successfully!', 'success')
        return redirect(url_for('login'))

    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
