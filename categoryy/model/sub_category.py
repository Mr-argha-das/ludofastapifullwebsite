from mongoengine import Document, StringField, IntField
from pydantic import BaseModel

class SubCategoryTable(Document):
    maincategoryid = StringField(required=True)
    price = StringField(required=True)
    totalplayer = IntField(required=True)

class SubCategoryModel(BaseModel):
    maincategoryid : str
    price : str
    totalplayer : str