# -*- coding: utf-8 -*-

from sqlalchemy import Column, Integer, String, Text, DateTime
from flaski.database import Base
from datetime import datetime

class WikiContent(Base):
	__tablename__ = 'wikicontents'
	id = Column(Integer, primary_key = True)
	title = Column(String(128), unique = True)
	body = Column(Text)

	def __init__(self,  title = None, body = None, president = None, establish = None, date = None):
		self.title = title
		self.body = body

	def __repr__(self):
		return '<Title %r>' % (self.title)
