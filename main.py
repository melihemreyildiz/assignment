from datetime import datetime, timedelta
from fastapi import FastAPI, status, HTTPException
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount

import serializers
from database import SessionLocal
import models
import requests
import base64
from requests.structures import CaseInsensitiveDict
from serializers import AdIm, AdCreative, Adset, Campaign

app = FastAPI()


#access_token = 'EAAGObqCO8AEBAJ7FZAoPtpibjjkqe5PgFZAa6DJ7jhWSg2IowFD\
#ZCslZAzmfM1nGZB9JKnMWSYk6j7oHz2FSMFCpJOhkGSH\
#ZAOH80BYvetZAw17SpjLdGLkABfPZCPAvzmZCC7GeiUyMtkIe4sMtZCqSxk1xV\
#OkoYowkHCyCHT9vW1wSun9seL4L4bXc0t5eXtZA30ZD'

access_token = 'EAAGObqCO8AEBAId1nSz6MkWaPLmZCudsdlljGnRfzufy8aDdss03Lu2isaJWZCIrVk8n7Xca6sF5ikUs7xCtBy\
Qps78Avj8NPn810O96ZAFqqL31wV9qsoZAOFGFUwo1ZAULkMUGsqcPc9OKRZAS5TuXlSHbF1c8mYdGCFfK\
ZBU5RgJrtVBem2mUn2bD9tMDXAZD'

ad_account_id = 'act_3061829570753376'
app_secret = 'ff2002ad9af7137b75aafe9e828571e8'
app_id = '438080767979521'
page_id = '104413048775500'

FacebookAdsApi.init(app_id=app_id, app_secret=app_secret, access_token=access_token)
ad_account = AdAccount(ad_account_id)

file_name = "gucci-bag.jpg"
headers = CaseInsensitiveDict()
headers["Accept"] = "application/json"
headers["Authorization"] = f"Bearer {access_token}"


db = SessionLocal()


@app.post("/create-campaign", status_code=status.HTTP_201_CREATED)
def create_campaign(item: Campaign | None = None):
    if item.name:
        db_item = db.query(models.Campaign).filter(models.Campaign.name == item.name).first()
        if db_item is not None:
            raise HTTPException(status_code=400, detail="Item already exists")
    if not item.name:
        db_item = db.query(models.Campaign).filter(models.Campaign.name == 'Conversions Campaign Melih').first()
        if db_item is not None:
            raise HTTPException(status_code=400, detail="Item already exists")
    fields = ['name', 'objective']
    params = {
        'name': 'Conversions Campaign Melih' if not item.name else item.name,
        'objective': 'REACH' if not item.name else item.name,
        'status': 'PAUSED',
        'special_ad_categories': [],
    }
    campaign:item = AdAccount(ad_account_id).create_campaign(
        fields=fields,
        params=params)

    if campaign:
        val = models.Campaign(
            id = campaign['id'],
            name = campaign['name'],
            objective= campaign['objective']
        )
        db.add(val)
        db.commit()

        return {'data': f'Succesfully Created:{campaign}'}
    return {'error': 'An error occurred'}


@app.post("/create-adset",status_code=status.HTTP_201_CREATED)
async def create_adset(item: Adset | None = None):
    if item.name:
        db_item = db.query(models.Campaign).filter(models.Campaign.name == item.name).first()
        if db_item is not None:
            raise HTTPException(status_code=400, detail="Item already exists")
    if not item.name:
        db_item = db.query(models.Campaign).filter(models.Campaign.name == 'AdSet').first()
        if db_item is not None:
            raise HTTPException(status_code=400, detail="Item already exists")

    fields = ['id', 'name', 'campaign_id', 'lifetime_budget', 'daily_budget', 'start_time', 'end_time',
              'targeting', 'bid_amount', 'status', 'optimization_goal']

    now = datetime.now()

    params = {
        'name': 'AdSet' if not item.name else item.name,
        'daily_budget': 2000,
        'start_time': now,
        'end_time': now + timedelta(days=10),
        'campaign_id': '120330000091598609' if not item.campaign_id else item.campaign_id,
        'bid_amount': 5,
        'billing_event': 'IMPRESSIONS',
        'optimization_goal': 'REACH',
        'targeting': {'age_min': 20,
                      'age_max': 35,
                      'geo_locations': {
                          'countries': ['AE', 'SA', 'KW'],
                          "location_types": [
                              "home"
                          ]
                      },
                      'facebook_positions': ['story']},
        'status': 'ACTIVE',
    }
    created_adset = AdAccount(ad_account_id).create_ad_set(fields=fields, params=params)

    if created_adset:
        values = Adset(**created_adset).dict()
        db_item = models.Adset(**values)
        db.add(db_item)
        db.commit()
        return {'data': f'Succesfully Created:{created_adset}'}


@app.post('/create-ads',status_code=status.HTTP_201_CREATED)
def create_ads(item: AdIm | None = None, val: AdCreative | None = None):
    hashed_value = None
    if not item:
        item = AdIm()
    if not val:
        val = AdCreative()

    try:
        with open(file_name, "rb") as f:
            #im_b64 = base64.b64encode(im_bytes).decode("utf8")
            files = {'upload_file': f}
            url = 'https://graph.facebook.com/v15.0/act_3061829570753376/adimages'
            response = requests.post(url=url, files=files, headers=headers)

        json_format = response.json()

        for i, j in json_format['images'].items():
            item.name = i
            item.hash = j["hash"]
            hashed_value = j["hash"]
            item.url = j["url"]
            db_item = models.AdIm(**item.dict())
            db.add(db_item)
            db.commit()
            break

        fields = ["id", "name", "object_story_spec"]

        params = {
            'name': 'Gucci AdCreative for Link Ad.',
            'object_story_spec': {'page_id': page_id,
                                  'link_data': {'image_hash': hashed_value,
                                                'link': 'https://www.ounass.ae/women/designers/gucci',
                                                'message': 'try it out'}},
        }

        ad_creative = AdAccount(ad_account_id).create_ad_creative(fields=fields, params=params)

        val.id = ad_creative["id"]
        val.name = ad_creative["name"]
        val.object_story_spec = {"link_data": {
            "image_hash": ad_creative["object_story_spec"]["link_data"]["image_hash"],
            "link": ad_creative["object_story_spec"]["link_data"]["link"],
            "message": ad_creative["object_story_spec"]["link_data"]["message"]
        },
            "page_id": ad_creative["object_story_spec"]["page_id"]
        }
        db_item_val = models.AdCreative(**val.dict())
        db.add(db_item_val)
        db.commit()

        return val

    except Exception as e:
        print(e)
        return {'error': str(e)}


@app.get("/adset-insight-api/{ad_set_id}", status_code=status.HTTP_200_OK)
def adset_insight_api(ad_set_id: int):
    try:
        url = f'https://graph.facebook.com/v15.0/{ad_set_id}/insights?fields=ad_impression_actions, clicks'
        json_format = requests.get(url, headers=headers).json()
        data = json_format["data"]
        if len(data) == 0:
            return {'body': None}
        else:
            return {'body': data[0]['body']}

    except Exception as e:
        return {"error": str(e)}


@app.get('/creative-preview-api/{creative_id}', status_code=status.HTTP_200_OK)
def creative_preview_api(creative_id: int):
    try:
        url = f'https://graph.facebook.com/v15.0/{creative_id}/previews?ad_format=DESKTOP_FEED_STANDARD'
        json_format = requests.get(url, headers=headers).json()
        data = json_format["data"]
        if len(data) == 0:
            return {'body': None}
        else:
            return {'body': data[0]['body']}

    except Exception as e:
        return {"error": str(e)}


@app.get('/')
def welcome():
    return {'ounass':'Ounass Assignment'}