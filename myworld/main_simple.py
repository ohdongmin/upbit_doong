import pyupbit
import time
from datetime import datetime
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
    send_line(msg)

def sell(ticker):
    time.sleep(0.1)
    balance = upbit.get_balance(ticker)
    s = upbit.sell_market_order(ticker, balance)
    current_price = pyupbit.get_current_price(target_ticker)
    msg = str(ticker)+"매도 완료"+str(current_price*balance)+"\n"+json.dumps(s, ensure_ascii = False)
    print(msg)
    send_line(msg)

def get_rsi(target_ticker, period=14):

    df = pyupbit.get_ohlcv(target_ticker, 'minute10')
    # 전일 대비 변동 평균
    df['change'] = df['close'].diff()

    # 상승한 가격과 하락한 가격
    df['up'] = df['change'].apply(lambda x: x if x > 0 else 0)
    df['down'] = df['change'].apply(lambda x: -x if x < 0 else 0)

    # 상승 평균과 하락 평균
    df['avg_up'] = df['up'].ewm(alpha=1/period).mean()
    df['avg_down'] = df['down'].ewm(alpha=1/period).mean()

    # 상대강도지수(RSI) 계산
    df['rs'] = df['avg_up'] / df['avg_down']
    df['rsi'] = 100 - (100 / (1 + df['rs']))
    rsi = df['rsi']

    return rsi.iloc[-1]

def send_line(msg):
    headers = {'Authorization':'Bearer '+token}
    message = {
        "message" : msg
    }
    requests.post(api_url, headers= headers , data = message)

def get_transaction_amount(date, num):
    tickers = pyupbit.get_tickers("KRW")	# KRW를 통해 거래되는 코인만 불러오기
    dic_ticker = {}
    for ticker in tickers:
        
        try :
            df = pyupbit.get_ohlcv(ticker, date)	# date 기간의 거래대금을 구해준다
            volume_money =  df['close'].iloc[-1] * df['volume'].iloc[-1]  
            dic_ticker[ticker] = volume_money
        except Exception as e:
            pass
     
    # 거래대금 큰 순으로 ticker를 정렬
    sorted_ticker = sorted(dic_ticker.items(), key= lambda x : x[1], reverse= True)
    coin_list = []
    count = 0
    for coin in sorted_ticker:
        count += 1
        # 거래대금이 높은 num 개의 코인만 구한다
        if count <= num:
            coin_list.append(coin[0])
        else:
            break
    return coin_list


def searchRSI(settingRSI):
    try :
        #tickers = get_transaction_amount(1,20)
        tickers = pyupbit.get_tickers(fiat="KRW")  #all finding
        for symbol in tickers : 
            rsi = get_rsi(symbol,14)
            if rsi < settingRSI :
                send_line("\n!!과매도 현상 발견!!\n"+symbol)
                print(f"{symbol} 매수 시점 rsi : {rsi}")
                time.sleep(1)
                return symbol
                
                
            #time.sleep(1)

    except :
        time.sleep(1)


# top5_tickers = get_transaction_amount("day", 5)	# 거래대금 상위 5개 코인 선정


load_dotenv()
access = os.environ["access"]  #access 키
secret = os.environ["secret"]  #secret 키
upbit = pyupbit.Upbit(access, secret)
api_url = "https://notify-api.line.me/api/notify"
token = os.environ["token"] # 앞서 발급 받은 토큰을 여기 넣음

# df = pd.read_csv('dataset.csv')
# ticker = "KRW-BTC"				       # 비트코인을 티커로 지정
# btc_day = pyupbit.get_ohlcv(ticker, interval="day")    # 비트코인의 일봉 정보
# balances = upbit.get_balances()
# my_money = float(balances[0]['balance'])    # 내 원화

trade_money =6000
while True:
    try : 
        target_RSI = 25
        sell_rsi = 60
        TF = False
        while TF == False:
            target_ticker = searchRSI(target_RSI)
            time.sleep(1)
            if len(target_ticker) > 1:
                buy(target_ticker,trade_money)
                bought_rsi = get_rsi(target_ticker,14)
                TF = True
                break
            else :
                print(f"계속 탐색중입니다. Target RSI : {target_RSI}")
                target_RSI += 1
        cnt = 1
        bp =False
        x = 0
        while TF == True :
            Coin_bought = upbit.get_balance(target_ticker)
            total_balance = Coin_bought * pyupbit.get_current_price(target_ticker) 
            rsi_value = get_rsi(target_ticker,14)
            print(f"매도 rsi : {rsi_value} ")
            if total_balance > 100000:
                send_line("매도 스킵합니다")
                bp = True
                break
            if Coin_bought<1:
                send_line('already sold')
                TF = False
                break
            if total_balance < trade_money*cnt*0.95:
                bp = True
                sell(target_ticker)
                break
            if rsi_value >60 :
                time.sleep(600)
                rsi_value = get_rsi(target_ticker,14)
                if rsi_value < sell_rsi -x:
                    sell(target_ticker)
                    TF = False
                    break
                else:
                    sell_rsi = max(rsi_value,sell_rsi)
                    if sell_rsi >=65:
                        x =2
                    elif sell_rsi>= 75:
                        x = 1
                    print(f'current rsi : {rsi_value}, waiting...')
            elif rsi_value < min(30,bought_rsi-2) and cnt <= 3: 
                bought_rsi -= 2
                buy(target_ticker,trade_money)
                send_line('buy more')
                cnt += 1
                time.sleep(300)
            else: 
                print("거래 조건 미충족")
                time.sleep(100)
        if bp ==True: 
            break
    except :
        time.sleep(1)
