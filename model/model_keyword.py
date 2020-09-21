"""
    @file: model/base_model.py
    @createdBy: Govind Savara
    @createdDate: 9/28/2016
    @lastModifiedBy: Govind Savara
    @lastModifiedDate: 9/30/2016
    @type: file
    @desc: model class for database tables
"""

from peewee import PrimaryKeyField, CharField, IntegerField, ForeignKeyField
from model.base_model import BaseModel


class Links(BaseModel):
    id = PrimaryKeyField()
    link = CharField()
    short_desc = CharField(max_length=150)
    description = CharField(max_length=500)


class KeywordsLink(BaseModel):
    id = PrimaryKeyField()
    keyword = CharField()
    link_id = ForeignKeyField(Links, related_name="Associated website")
    occurrence = IntegerField()



