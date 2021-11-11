from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from pathlib import Path
from sqlalchemy.sql.schema import ForeignKey

db_path = str(Path(__file__).parent / 'test.db')
db_url = f"sqlite+pysqlite:///{db_path}"
print(db_url)
engine = create_engine(db_url, echo=True, future=True)
Base = declarative_base()


class User(Base):
    __tablename__ = 'user_account'

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)
    mail = Column(String(100))


class Papers(Base):
    __tablename__ = 'papers'

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    abstract = Column(String, unique=True)


class UserInteractions(Base):
    __tablename__ = 'user_interactions'

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('user_account.id'))
    paper_id = Column(ForeignKey('papers.id'))
    decision = Column(String(30))


Base.metadata.create_all(engine)