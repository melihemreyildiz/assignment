from database import Base, engine
from models import Campaign,Adset,AdIm,AdCreative
import sqlalchemy


print("Creating database ....")

Base.metadata.create_all(engine)

