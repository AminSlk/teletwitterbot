from sqlalchemy import (Column, DateTime, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

from teletwitterbot.config import settings

Base = declarative_base()
engine = create_engine(settings["db_path"], echo=True)


class List(Base):  # pylint: disable=too-few-public-methods
    __tablename__ = 'lists'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    username = Column(String)
    members = relationship("Member", back_populates="list")
    last_check = Column(DateTime)


class Member(Base):  # pylint: disable=too-few-public-methods
    __tablename__ = 'members'
    id = Column(Integer, primary_key=True)
    list_id = Column(Integer, ForeignKey('lists.id'))
    username = Column(String)

    list = relationship("List", back_populates="members")


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
