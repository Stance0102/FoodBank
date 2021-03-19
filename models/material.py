from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from database import Base
import uuid
import datetime

class Material(Base):
	__tablename__ = 'material'
	Id = Column(String(50),primary_key=True)
	name = Column(String(50),nullable=True)
	quantity = Column(Integer(),default=0,nullable=True)
	create_datetime = Column(DateTime(),nullable=True)
	create_user_id = Column(String(50),ForeignKey('person.Id'),nullable=True)
	create_user_name = Column(String(50),nullable=True)
	change_id = Column(String(50))
	change_name = Column(String(50))
	final_datetime = Column(DateTime())
	role = Column(String(10),nullable=True)
	status = Column(Boolean(),nullable=True)
	view = Column(Boolean(),nullable=True)

	def __init__(self,name,quantity,create_user_id,create_user_name,role):
		self.Id = str(uuid.uuid4())
		self.name = name
		self.quantity = quantity
		self.create_datetime = datetime.datetime.now()
		self.create_user_id = create_user_id
		self.create_user_name = create_user_name
		self.change_id = None
		self.change_name = None
		self.final_datetime = None
		self.role = role
		self.status = False
		self.view = True

	def __repr__(self):
		return '<Material %r>' % (self.name)