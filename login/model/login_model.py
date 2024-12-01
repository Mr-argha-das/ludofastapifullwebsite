from mongoengine import Document, StringField, FloatField, BooleanField
from pydantic import BaseModel

class LoginTable(Document):
    email = StringField(required=True)
    name = StringField(required=True)
    password = StringField(required=True)


class LoginBody(BaseModel):
    name : str
    
