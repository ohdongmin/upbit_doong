import pyupbit
import time
from datetime import datetime
from pytz import timezone
import pandas as pd
import json
from dotenv import load_dotenv # pip install python-dotenv9
import os
import requests

def sell(ticker):
    time.sleep(0.1)
    balance = upbit.get_balance(ticker)
    current_price = pyupbit.get_current_price(ticker)
    sell_volume = round(current_price*balance,0)
    ror = round((current_price/upbit.get_avg_buy_price(ticker)-1)*100,2)
    msg = str(ticker)+"매도 완료"+str(sell_volume) + '\n' + "수익률 :" +str(ror) +"%"
    s = upbit.sell_market_order(ticker, balance)
    print(msg)
    send_line(msg)

def send_line(msg):
    headers = {'Authorization':'Bearer '+token}
    message = {
        "message" : msg
    }
    requests.post(api_url, headers= headers , data = message)

load_dotenv()
access = os.environ["access"]  #access 키
secret = os.environ["secret"]  #secret 키
upbit = pyupbit.Upbit(access, secret)
api_url = "https://notify-api.line.me/api/notify"
token = os.environ["token"] # 앞서 발급 받은 토큰을 여기 넣음

# sell('KRW-QKC')

sell('KRW-CVC')