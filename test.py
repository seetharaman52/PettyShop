from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# Creating Engine
db_url = "mysql://root:kit@1234@localhost/test"
engine = create_engine(db_url)
# Creating base
Base = declarative_base()
# Creating a model
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(100))
Base.metadata.create_all(engine)
# Creating a session
Session = sessionmaker(bind=engine)
session = Session()
# Creating objects
#new_user = User(username='seetharaman',email="cigar@duck.com")
#session.add(new_user)
#session.commit()
# Retrieve all users
# users = session.query(User).all()
# for user in users:
#     print(user.username)
# Retrieve users with a specific condition (e.g., username is 'seetharaman')
specific_user = session.query(User).filter_by(email='cigar@duck.com').first()
# if specific_user:
#     print(specific_user.id)
#     print(specific_user.username)
#     print(specific_user.email)

items = session.query(User).all()
for i in items:
    print("Name: {} Email: {}".format(i.username, i.email))
#Update a user's username
session.query(User).filter(User.username=="Seetharaman").update({"username":"Seetha"})
session.commit()
items = session.query(User).all()
for i in items:
    print("Name: {} Email: {}".format(i.username, i.email))
# Update a user's email
#specific_user.email = 'new_email@example.com'
#session.commit()
# Delete a user
#session.delete(specific_user)
#session.commit()

