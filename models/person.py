from sqlalchemy import Column, Integer, String, DateTime
from database import Base
from sqlalchemy.orm import relationship
import uuid
import datetime

class Member(Base):
	__tablename__ = 'person'
	Id = Column(String(50), primary_key=True)
	name = Column(String(50), unique=True, nullable=False)
	email = Column(String(60), unique=True, nullable=False)
	password = Column(String(50), nullable=False)
	address = Column(String(50), nullable=True)
	role = Column(String(10), nullable=True)
	join_datetime = Column(DateTime(), nullable=True)
	material = relationship(
		'Material',
		backref = 'person',
		cascade = 'all,delete'
	)

	def __init__(self,name,email,password,address,role):
		self.Id = str(uuid.uuid4())
		self.name = name
		self.email = email
		self.password = password
		self.address = address
		self.role = role
		self.join_datetime = datetime.datetime.now()

	def __repr__(self):
		return '<Member %r>' % (self.name)