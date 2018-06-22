from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from app.models import User



class LoginForm(FlaskForm):
    userName = StringField('User name', validators = [DataRequired()])
    password = PasswordField('Password',validators = [DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')



class RegistrationForm(FlaskForm):
    userName = StringField('User name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, userName):
        user = User.query.filter_by(userName=userName.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')


    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email.')



class EditProfileForm(FlaskForm):
    userName = StringField('User name', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_userName, *args, **kwargs):
        super(EditProfileForm,self).__init__(*args, **kwargs)
        self.original_userName = original_userName

    def validate_userName(self, userName):
        if userName.data != self.original_userName:
            user = User.query.filter_by(userName=userName.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')
