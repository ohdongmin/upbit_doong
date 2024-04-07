import pyupbit
import time
import datetime  # 변경한거 체크 하셈
from pytz import timezone
import pandas as pd
import json
from dotenv import load_dotenv # pip install python-dotenv
import os
import requests


def buy(ticker, money):
    time.sleep(0.1)
    b = upbit.buy_market_order(ticker, money)
    try:
        if b['error']:
            b = upbit.buy_market_order(ticker, 100000)
            msg = "error " + str(ticker)+" "+str(100000)+"원 매수시도"+"\n"+json.dumps(b, ensure_ascii = False)
    except:
        msg = str(ticker)+" "+str(money)+"원 매수완료"+"\n"+json.dumps(b, ensure_ascii = False)
    print(msg)


def sell(ticker):
    time.sleep(0.1)
    balance = upbit.get_balance(ticker)
    s = upbit.sell_market_order(ticker, balance)
    current_price = pyupbit.get_current_price(ticker)
    msg = str(ticker)+"매도 완료"+str(current_price*balance)+"\n"+json.dumps(s, ensure_ascii = False)
    print(msg)

def send_line(msg):
    headers = {'Authorization':'Bearer '+token}
    message = {
        "message" : msg
    }
    requests.post(api_url, headers= headers , data = message)

###변동성 돌파 전략(골든 크로스)
# 변동성 돌파 전략으로 매수 목표가 조회
def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price
# 시작 시간 조회
def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma10(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=15)
    ma10 = df['close'].rolling(10).mean().iloc[-1]
    return ma10

def get_ma10_pre(ticker):
    pre = datetime.datetime.now() - datetime.timedelta(minutes=10)
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=15, to= pre)
    ma10 = df['close'].rolling(10).mean().iloc[-1]
    return ma10

def get_ma30(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=45)
    ma30 = df['close'].rolling(30).mean().iloc[-1]
    return ma30
# 이전 5분봉 차트 7일 이동 평균선 조회(하락 판단)
def get_ma30_pre(ticker):
    pre = datetime.datetime.now() - datetime.timedelta(minutes=10)
    df = pyupbit.get_ohlcv(ticker, interval="minute10", count=45, to= pre)
    ma30 = df['close'].rolling(30).mean().iloc[-1]
    return ma30


load_dotenv()
access = os.environ["access"]  #access 키
secret = os.environ["secret"]  #secret 키
upbit = pyupbit.Upbit(access, secret)
api_url = "https://notify-api.line.me/api/notify"
token = os.environ["token"] # 앞서 발급 받은 토큰을 여기 넣음

while True:
    try:
        while True:
            ticker = 'KRW-BTC'
            ma10 = get_ma10(ticker)
            time.sleep(1)
            ma10_pre = get_ma10_pre(ticker)
            time.sleep(1)
            ma30 = get_ma30(ticker)
                
            if ma10 / ma30 >= 1.0  and ma10_pre < ma10 :
                buy(ticker,6000)
                break
            else:
                print('골든 크로스 대기 중') 
                time.sleep(300)

        while True:
            ma10 = get_ma10(ticker)
            time.sleep(1)
            ma30 = get_ma30(ticker)
            if ma30 > ma10 :
                sell(ticker) # 테스트 중
                break
            else:
                print('데드 크로스 대기중')
                time.sleep(300)
    
    except Exception as e:
        print(e)
        time.sleep(60)