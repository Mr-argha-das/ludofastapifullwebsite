from mongoengine import Document, StringField, IntField
from pydantic import BaseModel

class PassbookTable(Document):
    userid = StringField(required=True)
    title = StringField(required=True)
    amount = StringField(required=True)
    cre_date = StringField(required=True)
    
class PassBookBody(BaseModel):
    userid : str
    title : str
    amount : str
