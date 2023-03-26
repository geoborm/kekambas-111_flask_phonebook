from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone_number = db.Column(db.String(15), nullable=False) # (###) ###-####
    address = db.Column(db.String(100))    

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Address {self.id}|{self.first_name} {self.last_name}>"
    
    def edit(self, first_name, last_name, phone_number, address):
        self.first_name = first_name 
        self.last_name = last_name 
        self.phone_number = phone_number 
        self.address = address 
        db.session.add(self)
        db.session.commit()

user_address = db.Table('user_address',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
                        db.Column('address_id', db.Integer, db.ForeignKey('address.id'))
)


class User (db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(75), nullable=False, unique=True)
    username = db.Column(db.String(75), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    address = db.relationship('Address', secondary = user_address, backref='user_address', lazy = 'dynamic',cascade ='all, delete-orphan',
    single_parent=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.password = generate_password_hash(kwargs.get('password'))
        db.session.add(self)
        db.session.commit()
        
    def __repr__(self):
        return f"<User {self.id}|{self.username}>"
    
    def check_password(self, password_guess):
        return check_password_hash(self.password, password_guess)
    
    def add_addee(self, u_address):
        self.address.append(u_address)
        db.session.commit()

    def remove_addee(self, u_address): 
        self.address.remove(u_address)
        db.session.commit()

@login.user_loader
def get_a_user_by_id(user_id):
    return db.session.get(User, user_id)




    
# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(50), nullable=False)
#     last_name = db.Column(db.String(50), nullable=False)
#     email = db.Column(db.String(75), nullable=False, unique=True)
#     username = db.Column(db.String(75), nullable=False, unique=True)
#     password = db.Column(db.String(255), nullable=False)
#     date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     posts = db.relationship('Post', backref='author')

#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#         self.password = generate_password_hash(kwargs.get('password'))
#         db.session.add(self)
#         db.session.commit()

#     def __repr__(self):
#         return f"<User {self.id}|{self.username}>"

#     def check_password(self, password_guess):
#         return check_password_hash(self.password, password_gu

