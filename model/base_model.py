"""
    @file: model/base_model.py
    @createdBy: Govind Savara
    @createdDate: 9/28/2016
    @lastModifiedBy: Govind Savara
    @lastModifiedDate: 9/29/2016
    @type: file
    @desc: model class for database tables
"""

from peewee import Model, MySQLDatabase
from settings import DATABASE, MEDITAB_DATABASE

# initialize the database connection
db = MySQLDatabase(MEDITAB_DATABASE, user="root", password="root".encode("utf-8"))


# parent class for all model tables
class BaseModel(Model):
    class Meta:
        database = db

    @ staticmethod
    def db_create_record(data, table_name):
        """ creates records for the data in database table

        Args:
            data (dict): The record dict to be inserted in table.
            table_name (Model): The model instance of the table in which the record is to be inserted

        Returns:
            Model.tuple : The tuple has two records. First record is the id of the record inserted. Second
                          record is boolean indicating whether the record is already present or it
                          is inserted now. True indicates the record is inserted now.
        """
        try:
            slot = table_name.get_or_create(**data)
            print(slot)
            return slot
        except Exception as ex:
            print(ex)
            return