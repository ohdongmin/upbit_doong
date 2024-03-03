#-*- coding:utf-8 -*-

import pyupbit
import datetime
import numpy as np
import os

access = "wh097D7LzaGLtk8jvybLxuxDqtcHRXyZde3CE9dK"                         # Upbit API access 키
secret = "MCEq01J8Ha8TJ8WTIBAG99wFPwfow8DoEMnhvwmp"                          # Upbit API secret 키

# 내 잔고 조회_시작
def get_balance(ticker):
      balances = upbit.get_balances()
      for b in balances:
          if b['currency'] == ticker:
              if b['balance'] is not None:
                  return float(b['balance'])
              else:
                  return 0
# 내 잔고 조회_끝

# 로그인_시작
try:
  upbit = pyupbit.Upbit(access, secret)
  my_Balance = get_balance("KRW")             # 내 잔고
  print("Login OK")
  print("==========Autotrade start==========")
except:
  print("!!Login ERROR!!")
# 로그인_끝
else:
  print("내 잔고 : "+str(format(int(my_Balance),','))+" 원")
  print("date:"+str(datetime.datetime.now()))

# 원화 시장 티커목록 조회
krw_tickers = pyupbit.get_tickers("KRW")
print("== 원화(KR) 시장의 종목을 조회합니다 ==")
print("")
print("종목 리스트 : ", krw_tickers)
print("종목 개수 : ", len(krw_tickers))