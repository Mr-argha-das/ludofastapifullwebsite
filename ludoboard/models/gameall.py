from mongoengine import Document, StringField, FloatField
from pydantic import BaseModel

class GamePlayedTable(Document):
    userid = StringField(required=True)
    
class WithdrawalModel(BaseModel):
    userid : str
    ammount : int