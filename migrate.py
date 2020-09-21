from model.base_model import db
from model.model_keyword import (Links, KeywordsLink)

db.create_tables([Links, KeywordsLink])
db.register_fields({'primary_key': 'INT AUTOINCREMENT'})