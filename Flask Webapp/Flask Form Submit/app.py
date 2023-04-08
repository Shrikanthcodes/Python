from flask import Flask, render_template, request, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from flask_wtf import Form
from wtforms import TextField, IntegerField, TextAreaField, SubmitField, RadioField, SelectField
from wtforms import validators, ValidationError


app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisisasecret!'


class LoginForm(FlaskForm):
    id = StringField('id')
    retino = RadioField('Retinopathy', choices=[('y', 'Yes'), ('n', 'No')], default='n')
    comments = StringField('comments')



class ContactForm(Form):
    name = TextField("Name Of Student", [validators.Required("Please enter your name.")])
    Gender = RadioField('Gender', choices=[('M', 'Male'), ('F', 'Female')])
    Address = TextAreaField("Address")
    email = TextField("Email", [validators.Required("Please enter your email address."),
                                validators.Email("Please enter your email address.")])
    Age = IntegerField("age")
    Diabetic = SelectField('Languages', choices=[('y', 'Yes'), ('n', 'No')])

@app.route('/', methods=['GET', 'POST'])
def form():
    form = LoginForm()

    if form.validate_on_submit():
        return '<h1>The patient ID is {}. The doctor\'s diagnosis is {}.'.format(form.id.data, form.comments.data)
    return render_template('upload1.html', form=form)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form2 = ContactForm()

    if request.method == 'POST':
        if form2.validate_on_submit() == False:
            flash('All fields are required.')
            return render_template('upload.html', form=form2)
    elif request.method == 'GET':
        return render_template('upload.html', form=form2)
    if form2.validate_on_submit():
        return '<h1>The patient name is {}. The patient\'s gender is {}.'.format(form2.name.data, form2.Gender.data)
    return render_template('upload.html', form= form2)


if __name__ == "__main__":
    app.run(port=4555, debug=True)
