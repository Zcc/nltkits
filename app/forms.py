# ! /usr/bin/env python
# coding=utf-8
from flask.ext.wtf import Form
from wtforms import StringField, FileField, SelectField
from wtforms.validators import DataRequired


class myForm(Form):
    file = FileField('', validators=[DataRequired()])
    colnum = StringField('Column:', validators=[DataRequired()])
    fre = SelectField('task:', choices=[
                      ('ex', u'文本提取'), ('fr', u'词频统计'), ('sy', u'同义词扩展'), ('al', u'别称扩展')])
