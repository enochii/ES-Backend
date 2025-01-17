from sqlalchemy import create_engine
import pymysql
pymysql.install_as_MySQLdb()

from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

PRODUCT_PER_PAGE = 8

# Windows 记得换成 ///
# engine = create_engine('sqlite:///db/web.db', convert_unicode=True)

# mysql+mysqldb://<user>:<password>@<host>[:<port>]/<dbname>
engine = create_engine('mysql+mysqldb://web:web@47.98.247.28:3306/webdb', convert_unicode=True)

db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    # import all modules here that might define models so that
    # they will be registered properly on the metadata.  Otherwise
    # you will have to import them first before calling init_db()
    Base.metadata.create_all(bind=engine)

