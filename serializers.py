from typing import Optional, Any, List
from pydantic import BaseModel, Json, HttpUrl
from datetime import datetime


class Locations(BaseModel):
    countries: Optional[List[str]] = None
    location_types: Optional[List[str]] = None


class Targeting(BaseModel):
    age_max: Optional[int] = None
    age_min: Optional[int] = None
    facebook_positions: Optional[List[str]] = None
    geo_locations: Optional[Locations] = None


class Campaign(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    objective: Optional[str] = None

    class Config:
        orm_mode = True


class Adset(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    campaign_id: Optional[str] = None
    lifetime_budget: Optional[str] = None
    daily_budget: Optional[str] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    targeting: Optional[Targeting] = None
    bid_amount: Optional[int] = None
    status: Optional[str] = None
    optimization_goal: Optional[str] = None

    class Config:
        orm_mode = True


class AdIm(BaseModel):
    id: Optional[int] = None
    name: Optional[str] = None
    hash: Optional[str] = None
    url: Optional[str] = None

    class Config:
        orm_mode = True


class AdCreative(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    object_story_spec: Json[Any] = None

    class Config:
        orm_mode = True


