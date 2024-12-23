from mongoengine import Document, StringField, IntField
from pydantic import BaseModel

class UserUPITable(Document):
    userid =  StringField(required=True)
    upiId = StringField(required=True)
    
class UserUPIModel(BaseModel):
    userid : str
    upiId : str