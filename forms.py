from flask_wtf import FlaskForm
from flask_wtf import Form
from wtforms import StringField, TextField, SubmitField, IntegerField,TextAreaField,RadioField,SelectField, DecimalField
from wtforms.validators import DataRequired
from wtforms.validators import Length
from wtforms.validators import ValidationError

class PredictForm(FlaskForm):
   patient_age_quantile = IntegerField('Age')
   patient_addmited_to_regular = IntegerField('Regular')
   patient_addmited_to_semi_intense = IntegerField('Semi_intense')
   patient_addmited_to_intense = IntegerField('Intense')
   platelets = DecimalField('Platelets')
   mean_platelet_volume = DecimalField('mpv')
   red_blood_cells = DecimalField('rbc')
   lymphocytes = StringField('Lymphocytes')
   mean_corpuscular_hemoglobin_concentration = DecimalField('mchc')
   leukocytes = DecimalField('Leukocytes')
   basophils = DecimalField('Basophils')
   eosinophils = DecimalField('Eosinophils')
   mean_corpuscular_volum = DecimalField('mcv')
   monocytes = DecimalField('Monocytes')
   red_blood_cell_distribution_width = DecimalField('rbcdw')
   antigen = IntegerField('Antigen')
   submit = SubmitField('Predict')
   abc = ""
   confi = ""# this variable is used to send information back to the front page
