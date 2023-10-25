from connect import db
from mongoengine import *

from mongoengine.fields import ListField, StringField, ReferenceField

    
class Author(Document):
    fullname = StringField(required=True)
    born_date = StringField(max_length=50)
    born_location = StringField()
    description = StringField()
    # meta = {'allow_inheritance': True}


class Quote(Document):
    tags = ListField(StringField()) # list of fields 
    author = ReferenceField(Author, reverse_delete_rule=CASCADE) # (foregin key)
    quote = StringField(required=True)
    # meta = {'allow_inheritance': True}
