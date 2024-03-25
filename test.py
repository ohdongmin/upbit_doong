#-*- coding:utf-8 -*-

import pyupbit
import datetime
import numpy as np
import os
import pandas as pd

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
print(get_balance('KRW'))
# 로그인_시작
try:
  upbit = pyupbit.Upbit(access, secret)
  my_Balance = get_balance("KRW")             # 내 잔고
  print("Login COMPLETE")
  print("====================================")
except:
  print("!!Login ERROR!!")
# 로그인_끝
else:
  print("내 잔고 : "+str(format(int(my_Balance),','))+" 원")
  print("date:"+str(datetime.datetime.now()))

# # 원화 시장 티커목록 조회
# krw_tickers = pyupbit.get_tickers("KRW")
# print("== 원화(KR) 시장의 종목을 조회합니다 ==")
# print("")
# print("종목 리스트 : ", krw_tickers)
# print("종목 개수 : ", len(krw_tickers))

#시장가 매수 
# print(upbit.buy_market_order("KRW-DOGE", 6000))

#지정가 주문, 시장가 주문 #시장가는 금액단위, 지정가는 개수단위
print(upbit.sell_limit_order("KRW-XRP", 600, 20)) # 지정가 매도 (리플, 600원, 20개)
print(upbit.buy_limit_order("KRW-XRP", 613, 10)) # 지정가 매수 (리플, 613원, 10개) 
print(upbit.buy_market_order("KRW-XRP", 10000)) # 시장가 매수 (리플, 10,000원 매수)  
print(upbit.sell_market_order("KRW-XRP", 30)) # 시장가 매도 (리플, 30개 매도)


#주문취소
print(upbit.cancel_order('c5324fa8-056b-4b14-a0aa-3c6e9d596dcb'))
  
# print(upbit.buy_limit_order("KRW-BTC", 10000, 10)) # 지정가 매수 (리플, 613원, 10개) 
  
#미체결 내용 확인  
print(upbit.get_order("KRW-BTC")) 
  
#체결완료 내용 확인
print(upbit.get_order("KRW-DOGE", state = "done")) 


#거래 기록 표 만들기 미완성!!!
# columns = ['uuid', 'price', 'volume', 'market', 'created_at']
# od_info = pd.DataFrame(columns = columns)
# od_info.loc[0] = ['aa',20,10,'asd','asdf']
# order = upbit.buy_limit_order("KRW-BTC", 10000, 1)
# print(order)
# selected_data = {col: order[col] for col in columns}
# # df_append = pd.DataFrame(selected_data)
# # df_append.reset_index(drop=True, inplace=True)
# od_info.append(selected_data)
# # pd.concat([od_info,df_append], ignore_index = True)
# print(od_info)

#시장가 매도하기
print(upbit.sell_market_order("KRW-BTC", 0.0001))
get_balance("KRW")
