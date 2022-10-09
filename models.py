from sqlalchemy.sql.expression import null
from database import Base
from sqlalchemy import String,Boolean,Integer,Column,Text,DateTime, Sequence
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy_utils import URLType


class Campaign(Base):
    __tablename__ = 'campaignlist'
    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=True, unique=True)
    objective = Column(String(255), nullable=True)

    def __repr__(self):
        return f"<Campign name={self.name} objective={self.objective}>"


class Adset(Base):
    __tablename__ = 'adsetlist'
    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=True)
    campaign_id = Column(String(255))
    lifetime_budget = Column(String(255),nullable=True)
    daily_budget = Column(String(255),nullable=True)
    start_time = Column(String(255),nullable=True)
    end_time = Column(String(255),nullable=True)
    targeting = Column(JSON, nullable=True)
    bid_amount = Column(Integer, nullable=True)
    status = Column(String(255), nullable=True)
    optimization_goal = Column(String(255), nullable=True)


class AdIm(Base):
    __tablename__ = 'adim'
    id = Column(Integer, Sequence('adim_id',start=1, increment=1),primary_key=True)
    name = Column(String(255), nullable=True)
    hash = Column(String(255), nullable=True)
    url = Column(String(500),nullable=True)


class AdCreative(Base):
    __tablename__ = 'adcreativelist'
    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=True)
    object_story_spec = Column(JSON, nullable=True)
