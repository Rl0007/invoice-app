from peewee import *
import datetime
from flask_login import UserMixin

db = SqliteDatabase("invoice.db")


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel, UserMixin):
    email = CharField(unique=True)
    password = CharField()
    name = CharField()


class Customer(BaseModel):
    name = CharField()
    email = CharField(unique=True)
    phone = CharField()
    address = TextField()


class Item(BaseModel):
    name = CharField()
    price = DecimalField()


class Invoice(BaseModel):
    customer = ForeignKeyField(Customer, backref="invoices")
    date = DateField(default=datetime.date.today)
    total_amount = DecimalField(default=0.0)


def initialize_db():
    db.connect()
    db.create_tables([User, Customer, Item, Invoice], safe=True)
    db.close()
