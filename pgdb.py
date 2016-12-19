import os
from datetime import datetime

import yaml
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Text, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()
Base.to_dict = lambda self: {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Person(Base):
    __tablename__ = 'person'

    id = Column(Integer, primary_key=True)
    organization_id = Column(Integer, ForeignKey('organization.id'))
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, default='')
    phone = Column(String, nullable=False, default='')
    position = Column(String, nullable=False, default='')
    birthday = Column(DateTime, nullable=True)
    extra = Column(Text, nullable=False, default='')
    sending_email = Column(Boolean, nullable=False, default=True)
    date_added = Column(DateTime, nullable=False, default=datetime.now())
    date_modified = Column(DateTime, nullable=False, default=datetime.now(),
                           onupdate=datetime.now())
    organization = relationship('Organization', back_populates='people')


class Organization(Base):
    __tablename__ = 'organization'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String)
    email = Column(String)
    phone = Column(String)
    date_added = Column(DateTime, nullable=False, default=datetime.now())
    date_modified = Column(DateTime, nullable=False, default=datetime.now(),
                           onupdate=datetime.now())
    people = relationship('Person', back_populates='organization')


CWD = os.path.dirname(__file__)
with open(os.path.join(CWD, 'config.yml'), 'r') as config_file:
    cfg = yaml.load(config_file)

db = cfg['postgres']
engine = create_engine('postgresql://%s:%s@%s/%s' %
                       (db['username'], db['password'], db['host'], db['db']),
                       echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
