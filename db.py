"""
    Here we return data from Database which is mongoDB
"""

from pymongo import MongoClient
from bson.json_util import dumps, loads
from pydantic import BaseSettings
import json


#* Reading .env varaibles
class Settings(BaseSettings):

    DB_NAME: str
    DB_USER: str
    DB_HOST: str
    DB_PORT: int 
    DB_PASSWORD: str

    class Config:
        env_file = ".env"


db_config = Settings()
connectionString = f'mongodb://{db_config.DB_USER}:{db_config.DB_PASSWORD}@{db_config.DB_HOST}:{db_config.DB_PORT}/' if db_config.DB_USER and db_config.DB_PASSWORD \
    else f'mongodb://{db_config.DB_HOST}:{db_config.DB_PORT}/'

maxSevSelDelay = 1 
client = MongoClient(connectionString, serverSelectionTimeoutMS=maxSevSelDelay)
db = client.nestTest


def coinData(coinName:str =""):
    coins = db.coins
    if coinName:
        english = coins.find_one({'name': coinName.upper()})
        persian = coins.find_one({'persianName': coinName})
        usdt = coins.find_one({'name': "USDT"})
        if english :
            coinDatas = [english ,usdt]
            coins = list(coinDatas)
            data = dumps(coins,indent =2 )
            return data
        elif persian:
            coinDatas = [persian, usdt]
            coins = list(coinDatas)
            data = dumps(coins,indent =2 )
        else:
            return ""
        
    else:
        coins = list(coins.find())
        data = dumps(coins,indent =2 )
        print (data)
    return data

def priceTemplate(token: str = None) :
    header= "🔹🔸  نرخ لحظه ای خرید از صرافی باینکس  🔸🔹\n \
        .................................................... \n"
    footer=".................................................... \
        \n✅ :  افزایش قیمت در 30 دقیقه گذشته\
        \n 🛑:  کاهش قیمت در 30 دقیقه گذشته \
        \n...................................................."
    body=""
    result=""
    if coinData(token) :
        coins= json.loads(coinData(token))
        tokens = list(
            filter(lambda x: x['name'] != "USDT",coins)
        )
        USDT = list(
            filter(lambda x: x['name'] == "USDT",coins)
        )

        for coin in tokens:
            temp = "✅" if coin['pc1h'] >=0 else "🛑"
            temp += f" {coin['persianName']}: {round(coin['price'], coin['decimal'])} دلار - {int(coin['price'] * USDT[0]['price'])} تومان \n"
            
            body += temp
        if body:
            result = header + body + footer
        return result
    else :
        return ""