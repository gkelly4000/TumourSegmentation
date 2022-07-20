from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, FileField, IntegerField, DateTimeField, MultipleFileField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email

class LoginForm(FlaskForm):
    username = StringField("Username: ", validators=[DataRequired(), Length(min=5, max=50)])
    password = PasswordField("Password: ", validators=[DataRequired(), Length(min=8, max=80)])

    submit = SubmitField('Login')

class RegisterUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=80)])
    
    submit = SubmitField('Register User')

class RegisterPatientForm(FlaskForm):
    patientName = StringField('PatientName', validators=[DataRequired(), Length(min=5, max=50)])
    dob = DateField('DoB', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    postcode = StringField('Postcode', validators=[DataRequired(), Length(min=5, max=15)])
    city = StringField('City', validators=[DataRequired(), Length(min=5, max=50)])
    telephone = StringField('Telephone', validators=[DataRequired(), Length(min=10, max=20)])

    submit = SubmitField('Register Patient')

class RegisterDoctorForm(FlaskForm):
    doctorName =StringField('DoctorName', validators=[DataRequired(), Length(min=5, max=50)])
    doctorTelephone = StringField('DoctorTelephone', validators=[DataRequired(), Length(min=10, max=20)])
    doctorEmail = StringField("DoctorEmail", validators=[DataRequired(), Email()])

    submit = SubmitField('Register Doctor')

class UploadScanForm(FlaskForm):
    image = MultipleFileField('image')
    modality = StringField('Modality', validators=[DataRequired()], default="Multi-Sequence")
    scanDateTime = DateField('ScanDateTime', validators=[DataRequired()])
    doctorID = IntegerField('DoctorID', validators=[DataRequired()])
    patientID = IntegerField('PatientID', validators=[DataRequired()])

    submit = SubmitField('Submit Scan')

class UploadTestScanForm(FlaskForm):
    testImage = MultipleFileField('Test Image (Please upload 4 sequences (flair.nii, t1.nii, t1ce.nii, t2.nii))')
    testMask = FileField('Segmentation Mask (seg.nii)')

    submit = SubmitField('Upload Test Scan')

class UpdatePatientForm(FlaskForm):
    patientID = IntegerField('PatientID', validators=[DataRequired()])
    patientName = StringField('PatientName', validators=[DataRequired(), Length(min=5, max=50)])
    dob = DateField('DoB', validators=[DataRequired()])
    address = StringField('address', validators=[DataRequired()])
    postcode = StringField('Postcode', validators=[DataRequired(), Length(min=5, max=15)])
    city = StringField('City', validators=[DataRequired(), Length(min=5, max=50)])
    telephone = StringField('Telephone', validators=[DataRequired(), Length(min=10, max=20)])

    submit = SubmitField('Register Patient')
