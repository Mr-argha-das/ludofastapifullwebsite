from mongoengine import Document, StringField
from pydantic import BaseModel

class MainCategoryTable(Document):
    title = StringField(required = True)
    image = StringField(required = True)

class MainCateGoryModel(BaseModel):
    title : str
    image : str