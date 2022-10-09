from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


#to local usage
#engine=create_engine(f"postgresql://postgres:public@localhost/ounass",echo=True)



#docker usage
engine=create_engine(f"postgresql://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}@{os.getenv('PG_HOST')}/ounass",echo=True)

Base=declarative_base()

SessionLocal=sessionmaker(bind=engine)