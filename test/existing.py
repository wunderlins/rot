from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

class rotationstyp(Base):
	__table__ = Table('rotationstyp', Base.metadata, autoload=True)

class log(Base):
	__table__ = Table('log', Base.metadata, autoload=True)

class rotblock(Base):
	__table__ = Table('rotblock', Base.metadata, autoload=True)

class permission(Base):
	__table__ = Table('permission', Base.metadata, autoload=True)

class color(Base):
	__table__ = Table('color', Base.metadata, autoload=True)

class notes(Base):
	__table__ = Table('notes', Base.metadata, autoload=True)

class module(Base):
	__table__ = Table('module', Base.metadata, autoload=True)

class personal(Base):
	__table__ = Table('personal', Base.metadata, autoload=True)

class setting(Base):
	__table__ = Table('setting', Base.metadata, autoload=True)

class perstyp(Base):
	__table__ = Table('perstyp', Base.metadata, autoload=True)

class rotationsort(Base):
	__table__ = Table('rotationsort', Base.metadata, autoload=True)

class action(Base):
	__table__ = Table('action', Base.metadata, autoload=True)

class rotation(Base):
	__table__ = Table('rotation', Base.metadata, autoload=True)

class rotation2person(Base):
	__table__ = Table('rotation2person', Base.metadata, autoload=True)

class user(Base):
	__table__ = Table('user', Base.metadata, autoload=True)

