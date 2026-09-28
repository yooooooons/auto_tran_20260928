#!/usr/bin/env python
# coding: utf-8

# In[1]:


#money_for_a_item_divider = 7
#money_for_buy_a_item = 200000   # temp variable

#LIST_senario_percent = [0.995, 1.02]
#LIST_senario_median_today_start_to_yesterday_end_price = [1.01, 1.01]
#LIST_transaction_money_cri = [10000000, 100000000]
#LIST_buy_ratio_cri = [1.0, 1.0]
#LIST_buy_margin = [0.003, 0.003]

'''
temp_no_0_1 = int(5)
temp_no_0_2 = temp_no_0_1 + 1
temp_no_0_3 = temp_no_0_2 + 1
temp_no_0_4 = temp_no_0_3 + 1
temp_no_0_5 = temp_no_0_4 + 1
temp_no_0_6 = temp_no_0_5 + 1
temp_no_0_7 = temp_no_0_6 + 1
temp_no_0_8 = temp_no_0_7 + 1
temp_no_0_9 = temp_no_0_8 + 1
temp_no_0_10 = temp_no_0_9 + 1
temp_no_0_11 = temp_no_0_10 + 1
temp_no_0_12 = temp_no_0_11 + 1
temp_no_0_13 = temp_no_0_12 + 1
temp_no_0_14 = temp_no_0_13 + 1
temp_no_0_15 = temp_no_0_14 + 1
temp_no_0_16 = temp_no_0_15 + 1
temp_no_0_17 = temp_no_0_16 + 1
'''



#로컬PC와 서버와의 시간차이 보상
#operating_env = "local"
operating_env = "server"

time_conpensation_factor = 0

if (operating_env == "local") :
    time_conpensation_factor = 0
elif (operating_env == "server") :
    time_conpensation_factor = 9


# In[2]:


import os
from pathlib import Path
from dotenv import load_dotenv

# 1. 현재 파이썬 파일(main.py 등)이 위치한 폴더의 절대 경로를 구합니다.
#current_folder = Path(__file__).resolve().parent   # 일반 .py 파일에서 구동시
#current_folder = Path(os.getcwd()).resolve()   # .ipynb(주피터 랩, 주피터 노트북 등) 파일에서 구동시

if "__file__" in locals() or "__file__" in globals():
    current_folder = Path(__file__).resolve().parent
else:
    current_folder = Path(os.getcwd()).resolve()



# 2. 현재 폴더 안에 있는 .env 파일의 정확한 경로를 지정합니다.
env_path = current_folder / ".env"

# 3. 지정한 경로의 .env 파일을 시스템 환경변수로 로드합니다.
load_dotenv(dotenv_path=env_path)


TOSS_CLIENT_ID = os.environ.get("TOSS_API_KEY")
TOSS_CLIENT_SECRET = os.environ.get("TOSS_APP_SECRET")


# In[3]:


import pandas as pd
import datetime  # 유효시간 계산을 위해 상단에 import 필요
from datetime import datetime as d_time
from datetime import timedelta
import requests
import time
import json
import traceback
import statistics

import uuid



# 판다스 출력 화면이 잘리지 않도록 설정 (콘솔 확인용)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)


# In[4]:


DIC_candi_company = { "005930" : "삼성전자", "000660" : "하이닉스", "402340" : "SK스퀘어", "005380" : "현대차", "055550" : "신한지주", "373220" : "LG에너지솔루션", "207940" : "삼성바이오로직스", "010140" : "삼성중공업",
                     "015760" : "한국전력", "035420" : "NAVER", "005490" : "포스코홀딩스", "018260" : "삼성에스디에스", "011790" : "SKC", "017670" : "SK텔레콤", "000270" : "기아", "032830" : "삼성생명", "000810" : "삼성화재", 
                     "009150" : "삼성전기", "028260" : "삼성물산", "006800" : "미래에셋증권", "068270" : "셀트리온", "086790" : "하나금융지주", "105560" : "KB금융", "034020" : "두산퓨얼셀",
                     "012330" : "현대모비스",  "009540" : "한국조선해양", "003550" : "LG", "034730" : "SK", "010060" : "OCI", "006400" : "삼성SDI"}

DIC_candi_top_semi_company = {"005930" : "삼성전자", "000660" : "하이닉스"}

DIC_candi_general_company = {"005380" : "현대차", "055550" : "신한지주", "373220" : "LG에너지솔루션", "207940" : "삼성바이오로직스", "010140" : "삼성중공업",
                             "015760" : "한국전력", "035420" : "NAVER", "005490" : "포스코홀딩스", "018260" : "삼성에스디에스", "011790" : "SKC", "017670" : "SK텔레콤", "000270" : "기아", "032830" : "삼성생명", "000810" : "삼성화재", 
                             "009150" : "삼성전기", "028260" : "삼성물산", "006800" : "미래에셋증권", "068270" : "셀트리온", "086790" : "하나금융지주", "105560" : "KB금융", "034020" : "두산퓨얼셀",
                             "012330" : "현대모비스",  "009540" : "한국조선해양", "003550" : "LG", "034730" : "SK", "010060" : "OCI", "006400" : "삼성SDI"}




'''
DIC_candi_company_ratio = { "005930" : 0.09, "402340" : 0.09, "005380" : 0.09, "055550" : 0.09, "373220" : 0.09, "207940" : 0.09, "010140" : 0.09,
                           "015760" : 0.09, "035420" : 0.09, "005490" : 0.09, "018260" : 0.09, "011790" : 0.09, "017670" : 0.09, "000270" : 0.09, "032830" : 0.09, "000810" : 0.09, 
                           "009150" : 0.09, "028260" : 0.09, "006800" : 0.09, "068270" : 0.09, "086790" : 0.09, "105560" : 0.09, "034020" : 0.09,
                           "012330" : 0.09,  "009540" : 0.09, "003550" : 0.09, "034730" : 0.09, "010060" : 0.09, "006400" : 0.09}

DIC_candi_company = {"055550" : "신한지주", "010140" : "삼성중공업",
                     "015760" : "한국전력", "035420" : "NAVER", "018260" : "삼성에스디에스", "011790" : "SKC", "017670" : "SK텔레콤", "000270" : "기아",
                     "006800" : "미래에셋증권", "068270" : "셀트리온", "086790" : "하나금융지주", "105560" : "KB금융", "034020" : "두산퓨얼셀",
                     "003550" : "LG", "010060" : "OCI"}

DIC_candi_company_ratio = {"055550" : 0.09, "010140" : 0.09, "015760" : 0.09,
                           "035420" : 0.09, "018260" : 0.09, "011790" : 0.09, "017670" : 0.09, "000270" : 0.09,
                           "006800" : 0.09, "068270" : 0.09, "086790" : 0.09, "105560" : 0.09, "034020" : 0.09,
                           "003550" : 0.09, "010060" : 0.09}
                     
'''


                



# In[5]:


# 관련 함수 정의


# OAuth2 토큰 발급
def get_access_token(TOSS_CLIENT_ID_insert, TOSS_CLIENT_SECRET_insert):

    token_BASE_URL = "https://openapi.tossinvest.com"
    
    """OAuth2 토큰 발급"""
    url = f"{token_BASE_URL}/oauth2/token"
    token_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    token_payload = {
        "grant_type": "client_credentials",
        "client_id": TOSS_CLIENT_ID_insert,
        "client_secret": TOSS_CLIENT_SECRET_insert,
    }
    response = requests.post(url, headers = token_headers, data = token_payload)
    
    token_request = response.json().get("access_token") or response.json().get("access_token")
    # access_token = response.json().get("access_token") or response.json().get("("accessToken")")

    expires_in = response.json().get("expires_in")


    issued_at = datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600))  # 클라우드 서버와 한국과의 시간차이 보정 (9시간)
    expires_at = issued_at + datetime.timedelta(seconds=int(expires_in))
            
    print(f"토큰 유효 기간: {expires_in}초 (약 {int(expires_in)/3600:.1f}시간)")
    print(f"토큰 만료 일시: {expires_at.strftime('%Y-%m-%d %H:%M:%S')}")

    
    return token_request

    

# 현재 보유중인 자산 확인 (현금, 종목, 수익율 등)
def asset_check (access_token_this_time) :

    # =====================================================================
    # 2. 계좌 잔고 조회 설정 정보
    # =====================================================================
    MY_ACCOUNT_NUMBER = "1"  # 본인의 토스증권 계좌번호 입력
    holdings_url = "https://openapi.tossinvest.com/api/v1/holdings"
    
    # =====================================================================
    # 3. HTTP Request Headers 및 Params 설정
    # =====================================================================
    headers = {
        "X-Tossinvest-Account": MY_ACCOUNT_NUMBER,  # 대소문자 정확히 일치
        "Authorization": f"Bearer {access_token_this_time}"
    }
    
    # 전체 보유 주식 및 예수금을 확인하려면 대개 params를 비우거나 
    # 가이드 문서의 다른 잔고 조회용 엔드포인트(예: /balances)가 있는지 확인이 필요할 수 있습니다.
    # 우선 가이드에 나온 기본 형태로 전체 조회를 시도합니다.
    params = {} 
    
    print("현재 계좌의 보유 자산 및 주식 상태를 조회합니다...")
    print(f"요청 URL: {holdings_url}\n")
    
    try:

        # -----------------------------------------------------------------
        # 1. 포맷팅 헬퍼 함수 정의 (문자열을 숫자 변환 후 천단위 콤마 및 % 적용)
        # -----------------------------------------------------------------
        def fmt_amt(val):
            """금액 포맷팅: 숫자로 변환 후 1,000 단위 콤마 추가"""
            if val is None or val == "": return "-"
            try:
                return f"{int(float(val)):,}"
            except ValueError:
                return val
    
        def fmt_rate(val):
            """수익률 포맷팅: 소수점 문자열을 % 단위로 변환 (예: -0.3744 -> -37.44%)"""
            if val is None or val == "": return "-"
            try:
                return f"{float(val) * 100:.2f}%"
            except ValueError:
                return val

        
        # GET 메서드를 사용하여 보유 현황 조회
        response = requests.get(holdings_url, headers=headers, params=params)

        # 4. 응답 결과 처리
        if response.status_code == 200:
            print("계좌 정보 조회가 완료되었습니다.")
            
            holdings_result = response.json()
            # 가독성 좋게 정렬된 JSON 데이터 출력
            print(json.dumps(holdings_result, indent=4, ensure_ascii=False))
            print("holdings_result : ", holdings_result)
            
            # [참고] 만약 특정 주식(예: 삼성전자)만 콕 집어서 확인하고 싶다면 아래와 같이 활용 가능합니다.
            # response_single = requests.get(holdings_url, headers=headers, params={"symbol": "005930"})

            result_data = holdings_result.get("result", {})

            print("result_data : ", result_data)
            
            # -----------------------------------------------------------------
            # 2. 계좌 요약 데이터프레임 생성
            # -----------------------------------------------------------------
            summary_data = {
                "항목": ["총 매수금액", "총 평가금액", "총 평가금액(제비용후)", "총 평가손익", "총 평가손익(제비용후)", "총 수익률", "총 수익률(제비용후)", "당일 평가손익", "당일 수익률"],
                "금액/비율": [
                    fmt_amt(result_data.get("totalPurchaseAmount", {}).get("krw")),
                    fmt_amt(result_data.get("marketValue", {}).get("amount", {}).get("krw")),
                    fmt_amt(result_data.get("marketValue", {}).get("amountAfterCost", {}).get("krw")),
                    fmt_amt(result_data.get("profitLoss", {}).get("amount", {}).get("krw")),
                    fmt_amt(result_data.get("profitLoss", {}).get("amountAfterCost", {}).get("krw")),
                    fmt_rate(result_data.get("profitLoss", {}).get("rate")),
                    fmt_rate(result_data.get("profitLoss", {}).get("rateAfterCost")),
                    fmt_amt(result_data.get("dailyProfitLoss", {}).get("amount", {}).get("krw")),
                    fmt_rate(result_data.get("dailyProfitLoss", {}).get("rate"))
                ]
            }
            df_summary = pd.DataFrame(summary_data)
            
            print("[계좌 자산 요약]")
            print(df_summary.to_string(index=False))
            print("-" * 50)
        
            # -----------------------------------------------------------------
            # 3. 개별 보유 주식 데이터프레임 생성
            # -----------------------------------------------------------------
            items = result_data.get("items", [])
            if items:
                item_list = []
                for item in items:
                    item_list.append({
                        "종목명": item.get("name"),
                        "종목코드": item.get("symbol"),
                        "보유수량": fmt_amt(item.get("quantity")),
                        "매입단가": fmt_amt(item.get("averagePurchasePrice")),
                        "현재가": fmt_amt(item.get("lastPrice")),
                        "총매수금액": fmt_amt(item.get("marketValue", {}).get("purchaseAmount")),
                        "평가금액": fmt_amt(item.get("marketValue", {}).get("amount")),
                        "평가손익": fmt_amt(item.get("profitLoss", {}).get("amount")),
                        "수익률": fmt_rate(item.get("profitLoss", {}).get("rate")),
                        "당일손익": fmt_amt(item.get("dailyProfitLoss", {}).get("amount")),
                        "수수료": fmt_amt(item.get("cost", {}).get("commission")),
                        "제세금": fmt_amt(item.get("cost", {}).get("tax"))
                    })
                    
                df_items = pd.DataFrame(item_list)
                
                print("[보유 주식 상세 현황]")
                print(df_items.to_string(index=False))   

                
            else:
                print("현재 보유 중인 주식이 없습니다.")

                

            return holdings_result
    
            
        else:
            print(f"[조회 실패] 토스증권 API 서버에서 에러를 반환했습니다.")
            print(f"상태 코드 (Status Code): {response.status_code}")
            print(f"에러 내용: {response.text}")
    
    except Exception as e:
        print(f"[통신 에러] 요청 중 예기치 못한 오류가 발생했습니다: {e}")









def get_toss_cash_buyable(access_token_this_time):
    # 1. API 엔드포인트 URL 설정
    url = "https://openapi.tossinvest.com/api/v1/buying-power"

    # 2. 사용자 인증 정보 설정 (실제 본인의 값으로 변경하세요)
    # 보안을 위해 환경 변수나 설정 파일에서 가져오는 것을 권장합니다.
    TOSS_ACCOUNT_ID = "1"  # 가이드에 명시된 X-Tossinvest-Account 값
    SECRET_TOKEN = access_token_this_time  # 발급받은 API 비밀 토큰

    # 3. 요청 헤더 및 파라미터 구성
    headers = {
        "X-Tossinvest-Account": TOSS_ACCOUNT_ID,
        "Authorization": f"Bearer {SECRET_TOKEN}",
        "Accept": "application/json",  # JSON 응답을 명시적으로 요청
    }

    params = {
        "currency": "KRW",  # 대한민국 원화 기준 조회
    }

    try:
        # 4. API 서버에 GET 요청 보냄
        response = requests.get(url, headers=headers, params=params)

        # 5. HTTP 상태 코드 확인 (200이 아니면 예외 발생)
        response.raise_for_status()

        # 6. JSON 데이터 파싱 및 결과 출력
        data = response.json()
        
        # 'result' 안에서 'cashBuyingPower' 값을 가져옵니다.
        # 값이 없을 경우를 대비해 기본값 '0'을 설정합니다.
        buying_power_str = data.get('result', {}).get('cashBuyingPower', '0')
        
        # 문자로 된 금액을 숫자(정수)로 변환합니다 (예: '99999' -> 99999)
        buying_power_int = int(buying_power_str)
        
        print("\n[토스증권 API] 거래가능 금액 조회 성공")
        # : , 를 넣으면 3자리마다 쉼표가 찍힙니다 (예: 99,999원)
        #print(f"거래가능 금액: {buying_power_int:,} 원") 
        
        return buying_power_int
        

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 에러가 발생했습니다: {http_err}")
        print(f"서버 응답 내용: {response.text}")
    except requests.exceptions.RequestException as err:
        print(f"요청 중 에러가 발생했습니다: {err}")
    except ValueError:
        print("응답 데이터를 JSON으로 파싱하는 데 실패했습니다.")




















def get_1m_1d_candles(access_token_this_time, candle_type, symbol, No_candle, No_size):

    candle_BASE_URL = "https://openapi.tossinvest.com"
    
    url = f"{candle_BASE_URL}/api/v1/candles"
    headers = {"Authorization": f"Bearer {access_token_this_time}"}

    # 현재 시간 기준 ISO 8601 형식 설정
    current_before = (d_time.now() + timedelta(hours = time_conpensation_factor)).strftime("%Y-%m-%dT%H:%M:%S+09:00")

    all_candles = []
    total_needed = No_candle  # 5일치 1분봉 데이터 분량 (하루 약 390분 * 5일)
    chunk_size = No_size  # 토스증권 API 1회 최대 호출 제한량

    print(f"토스증권으로부터 1분봉 데이터 수집 시작 (목표: {total_needed}개)...")

    while len(all_candles) < total_needed:
        params = {
            "symbol": symbol,
            "interval": candle_type,  # 1분봉 요청
            "count": str(chunk_size),
            "before": current_before,
            "adjusted": "true",
        }

        response = requests.get(url, headers=headers, params=params)

        if response.status_code != 200:
            print(f"데이터 수집 중 에러 발생: {response.status_code}")
            break

        raw_data = response.json()
        result_node = raw_data.get("result", {})
        candles_chunk = result_node.get("candles", [])

        if not candles_chunk:
            print("종료: 더 이상 가져올 과거 데이터가 없습니다.")
            break

        all_candles.extend(candles_chunk)
        print(f"  -> 현재 {len(all_candles)}개 수집 완료...")

        # 다음 과거 데이터를 위해 before 시간 갱신
        last_candle_time = candles_chunk[-1].get("timestamp")
        if last_candle_time:
            current_before = last_candle_time
        else:
            break

        time.sleep(0.2)  # 연속 호출 제한 방지

    if not all_candles:
        print("수집된 데이터가 없습니다.")
        return None

    # 1. Pandas DataFrame 변환
    df = pd.DataFrame(all_candles)

    # 시간 컬럼 처리 및 인덱스 지정
    df["standard_time"] = pd.to_datetime(df["timestamp"])
    df.set_index("standard_time", inplace=True)

    # 중복 제거 및 과거 -> 현재 순 정렬
    df = df[~df.index.duplicated(keep="first")]
    df = df.sort_index()

    # 데이터 타입 숫자형으로 변환
    target_columns = ["openPrice", "highPrice", "lowPrice", "closePrice", "volume"]
    for col in target_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # 필요한 컬럼만 추출하고 한글 이름으로 변경
    df_clean = df[target_columns].copy()
    df_clean.columns = ["시가", "고가", "저가", "종가", "거래량"]

    return df_clean


# In[6]:


# 판매할 수 있는 물량 확인
def get_sellable_quantity(api_token, item_code) :
    """토스증권 API를 통해 보유 중인 종목의 판매 가능 수량을 조회합니다.

    :param api_token: 토스증권 API Secret Token (Bearer 토큰)
    :param account_id: 계좌 번호/식별자 (기본값: "1")
    :return: 판매 가능 수량 (정수)
    """
    url = "https://openapi.tossinvest.com/api/v1/sellable-quantity"

    headers = {
        "X-Tossinvest-Account": "1",
        "Authorization": f"Bearer {api_token}",
    }

    # 삼성전자 종목코드: 005930
    params = {"symbol": str(item_code)}

    try:
        response = requests.get(url, headers=headers, params=params)
        # HTTP 에러 발생 시 예외 호출 (4xx, 5xx)
        response.raise_for_status()

        data = response.json()

        # JSON 응답에서 sellableQuantity 추출 및 정수형(int) 변환
        sellable_qty_str = data.get("result", {}).get("sellableQuantity", "0")
        return int(sellable_qty_str)

    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 네트워크/HTTP 에러 발생: {e}")
        raise
    except (KeyError, ValueError) as e:
        print(f"응답 데이터 파싱 실패: {e}")
        raise






# 매수 함수 정의

def run_toss_stock_buyer_seller(access_token_this_time, transaction_company, transaction_side, price_type, transaction_quantity, transaction_price, company_dict = None):
    """
    토스증권 API를 이용한 지정가/시장가 매수/매도 주문 통합 함수
    """
    MY_ACCOUNT_SEQ = "1"
    order_url = "https://openapi.tossinvest.com/api/v1/orders"

    # HTTP 헤더 설정
    order_headers = {
        "X-Tossinvest-Account": MY_ACCOUNT_SEQ,
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token_this_time}"
    }

    # clientOrderId 중복(422 idempotency-key-conflict) 방지를 위해 UUID4 사용
    #unique_client_order_id = f"order-{uuid.uuid4().hex}"
    unique_client_order_id = f"order-{uuid.uuid4().hex[:16]}"

    # 주문 페이로드 구성
    order_payload = {
        "clientOrderId": unique_client_order_id,
        "symbol": str(transaction_company),
        "side": transaction_side.upper(),      # 'BUY' 또는 'SELL'
        "orderType": price_type,               # 'LIMIT' 또는 'MARKET'
        "quantity": str(transaction_quantity),
        "price": str(transaction_price),
    }

    # 종목명 출력용 (사전에 전달받지 못한 경우 종목코드 그대로 표시)
    company_name = company_dict.get(transaction_company, transaction_company) if company_dict else transaction_company
    side_name = "매수" if transaction_side.upper() == "BUY" else "매도"

    print(f"\n[{side_name} 주문 요청 중] {company_name}_{transaction_quantity}주_{transaction_price}원 (clientOrderId: {unique_client_order_id})")

    try:
        # API 요청 전송
        order_response = requests.post(order_url, headers=order_headers, json=order_payload, timeout=10)
        
        # JSON 응답 파싱 (파싱 에러 방지)
        try:
            response_json = order_response.json()
        except ValueError:
            response_json = {}

        print(f"[{side_name} 주문 접수 상태 확인]")

        # 성공 처리 (200 OK 또는 201 Created)
        if order_response.ok:  # status_code가 200~299 사이일 때 True
            print(f"{side_name} 주문 접수 성공!")
            
            # 응답 데이터 구조에 안전하게 접근
            toss_order_id = response_json.get("result", {}).get("orderId") or response_json.get("orderId", "UNKNOWN")
            print(f"order_result_data : {response_json}")
            print(f"toss_order_id : {toss_order_id}\n")
            
            return 1, toss_order_id

        # 실패 처리 (4xx, 5xx 에러)
        else:
            print(f"{side_name} 주문 실패 (상태 코드: {order_response.status_code})")
            print(f"응답 본문: {order_response.text}")
            
            # 에러 발생 시에도 혹시 모를 orderId 또는 error 정보 추출
            toss_order_id = response_json.get("result", {}).get("orderId", None)
            return 0, toss_order_id

    except requests.exceptions.RequestException as e:
        # 네트워크 에러, 타임아웃 등 요청 자체가 실패한 경우
        print(f"[{side_name} 주문 중 통신 예외 발생]: {e}")
        return 0, None










def get_orderbook(access_token_this_time, symbol_this_time):
    """
    특정 종목의 매수/매도 호가 및 잔량을 조회하는 함수
    
    :param symbol: 종목 심볼 (예: '005930', 'AAPL')
    :param access_token: 인증용 Bearer 토큰 (YOUR_SECRET_TOKEN)
    :return: 매도호가(asks) 목록과 매수호가(bids) 목록을 담은 딕셔너리
    """
    url = "https://openapi.tossinvest.com/api/v1/orderbook"
    
    headers = {
        "Authorization": f"Bearer {access_token_this_time}"
    }
    
    params = {
        "symbol": symbol_this_time
    }
    
    try:
        response = requests.get(url, headers=headers, params=params)
        
        # 요청 실패 시 예외 발생 (4xx, 5xx 에러)
        response.raise_for_status()
        
        data = response.json()
        result = data.get("result", {})
        
        # 매도 호가(asks)와 매수 호가(bids) 추출
        asks = result.get("asks", [])  # 매도 호가 (팔고자 하는 가격)
        bids = result.get("bids", [])  # 매수 호가 (사고자 하는 가격)
        
        return {
            "timestamp": result.get("timestamp"),
            "currency": result.get("currency"),
            "asks": asks,
            "bids": bids
        }

    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류가 발생했습니다: {e}")
        return None









def transaction_result_check (token_this_time, order_id) :

    MY_ACCOUNT_SEQ = "1"
    
    # ==========================================
    # [단계] 토스 서버가 준 ID로 체결 상태 조회
    # ==========================================
    check_url = f"https://openapi.tossinvest.com/api/v1/orders/{order_id}"

    order_headers = {
        "X-Tossinvest-Account": MY_ACCOUNT_SEQ,
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token_this_time}"
        }

    print(f"\n토스 주문 ID로 체결 상태를 확인합니다...")

    # 조회 API는 GET 방식을 사용하며, 주문할 때와 헤더가 동일합니다.
    check_response = requests.get(check_url, headers = order_headers)

    if check_response.status_code == 200:
        order_status_data = check_response.json()
        print("[조회 성공] 최종 주문 상태 결과:")
        print(json.dumps(order_status_data, indent=4, ensure_ascii=False))
        
        # 조회 데이터 역시 'result' 키 내부에 포장되어 오므로 안전하게 방어 코드를 작성합니다.
        status_info = order_status_data.get("result") if "result" in order_status_data else order_status_data
        
        status = status_info.get("status")
        
        # [버그 수정]: 'execution' 딕셔너리가 존재하면 그 안에서 진짜 체결 수량(filledQuantity)을 꺼내옵니다.
        execution_info = status_info.get("execution", {})
        if execution_info:
            filled_qty = execution_info.get("filledQuantity", "0")
        else:
            # 아직 체결 정보가 생기기 전(대기 상태 등)일 경우의 방어 코드
            filled_qty = status_info.get("filledQuantity", "0")

        
        print(f"\n현재 주문 상태: {status}")
        print(f"체결된 수량: {filled_qty}주")

        status_return = 0
        
        if status == "FILLED":
            print("주문의 체결이 완료되었습니다! 계좌를 확인해보세요.")
            status_return = 1
            return status_return
            
        elif status == "REJECTED":
            print("주문이 거부되었습니다. (이유: 예수금 부족, 주문 가능 시간 아님 등)")
            status_return = 5
            return status_return
            
        else:
            print("아직 주문이 체결되지 않고 호가창에 접수되어 대기 중입니다.")
            status_return = 0
            return status_return
            
    else:
        print(f"주문 상태 조회 실패 (상태 코드: {check_response.status_code})")
        print(check_response.text)


# In[7]:


# 체결이 되지 않은 상태의 주문에 대해 취소하는 처리

def cancel_toss_stock_order(access_token_this_time, order_id):
    """토스증권 API를 이용한 기존 주문 취소 함수

    :param access_token_this_time: 현재 유효한 OAuth Access Token (문자열)
    :param order_id: 취소할 주문의 식별자 (서버에서 발급받은 opaque token 문자열)
    """
    MY_ACCOUNT_SEQ = (
        "1"  # 계좌 조회 결과에 따른 순번(Sequence) 값 "1"을 지정합니다.
    )

    # URL 경로에 입력받은 order_id를 동적으로 삽입합니다.
    cancel_url = f"https://openapi.tossinvest.com/api/v1/orders/{order_id}/cancel"

    # HTTP 헤더 설정 (매수 함수와 동일한 규격)
    cancel_headers = {
        "X-Tossinvest-Account": MY_ACCOUNT_SEQ,
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token_this_time}",
    }

    print(f"\n[취소 요청] 주문 ID ({order_id}) 취소 진행 중...")

    # 공식 가이드에 따라 POST 요청을 보내며, 빈 json 객체({})를 전달합니다.
    try:
        response = requests.post(
            cancel_url, headers=cancel_headers, json={}
        )

        # 200(성공) 또는 201(생성됨) 상태 코드가 아니면 실패 처리
        if response.status_code not in [200, 201]:
            print(
                f"주문 취소 요청 실패 (상태 코드: {response.status_code})"
            )
            print(f"상세 에러 내용: {response.text}")
            return False

        # 성공 시 응답 데이터 파싱
        cancel_result = response.json()
        print("주문 취소 접수 성공!")
        return cancel_result

    except Exception as e:
        print(f"네트워크 또는 기타 에러 발생: {e}")
        return False










def get_stock_quantity(data, target_symbol) :
    # 2. 데이터 구조에 맞춰 'items' 리스트를 가져옵니다.
    items = data.get("result", {}).get("items", [])

    # 3. items 안의 주식들을 하나씩 꺼내며 검사합니다.
    for item in items:
        # 4. 찾고자 하는 종목번호(symbol)와 일치하는지 확인합니다.
        if item.get("symbol") == target_symbol:
            # 토스증권은 수량(quantity)을 문자열('100')로 주기 때문에 숫자로 변환합니다.
            quantity = int(item.get("quantity", 0))
            name = item.get("name")
            print(f"종목 검색 성공! [{name} / {target_symbol}]")
            print(f"현재 보유 수량: {quantity} 주")
            return quantity

    # 만약 리스트를 다 돌았는데도 찾지 못했다면 보유하지 않은 주식입니다.
    print(f"해당 종목번호({target_symbol})는 보유 중이 아닙니다.")
    return 0


# In[8]:


# 매수가격 호가 단위 반영 조정 함수 정의

def buyable_price_volume_with_unit (buy_intermediate_price, budget_for_buy_a_item) :
    
    buy_unit = 0
    
    if buy_intermediate_price < 2000 :
        buy_unit = 1
    elif (2000 <= buy_intermediate_price < 5000) :
        buy_unit = 5
    elif (5000 <= buy_intermediate_price < 20000) :
        buy_unit = 10
    elif (20000 <= buy_intermediate_price < 50000) :
        buy_unit = 50
    elif (50000 <= buy_intermediate_price < 200000) :
        buy_unit = 100
    elif (200000 <= buy_intermediate_price < 500000) :
        buy_unit = 500
    elif (500000 <= buy_intermediate_price) :
        buy_unit = 1000

    compensation_share = buy_intermediate_price // buy_unit
    buy_price = int(buy_unit * compensation_share)
    buy_volume = int(budget_for_buy_a_item // buy_price)

    return buy_price, buy_volume


# In[ ]:


# 거래 로직


cycle_period = 30

token_get = "temp"


transaction_money_criteria = 100000000
ratio_0801_to_0800_price_check_criteria = 0.995
ratio_0801_to_0800_price_buy_criteria = 0.99

print ("Program Begins\n")

total_cash_buyable_today = 0
money_for_a_item_divider_for_top_semi_comp = 2
money_for_a_item_divider_for_general_comp = 5

money_for_buy_a_top_semi_comp = 0
total_cash_buyable_residual = 0
total_cash_buyable_residual_s = 0
 
DIC_candi_top_semi_company_yesterday_end_price = {}
DIC_candi_general_company_yesterday_end_price = {}

DIC_candi_top_semi_company_0800_start_price = {}
DIC_candi_general_company_0800_start_price = {}

DIC_candi_top_semi_company_0801_start_price = {}
DIC_candi_general_company_0801_start_price = {}

DIC_candi_top_semi_company_0802_start_price = {}
DIC_candi_general_company_0802_start_price = {}

DIC_candi_company_ratio_top_semi_comp_0800_to_yesterday = {}
DIC_candi_company_ratio_general_comp_0800_to_yesterday = {}

DIC_candi_company_ratio_top_semi_comp_0801_to_yesterday = {}
DIC_candi_company_ratio_general_comp_0801_to_yesterday = {}

DIC_candi_company_ratio_top_semi_comp_0802_to_yesterday = {}
DIC_candi_company_ratio_general_comp_0802_to_yesterday = {}

DIC_candi_company_ratio_top_semi_comp_0801_to_0800 = {}
DIC_candi_company_ratio_general_comp_0801_to_0800 = {}

DIC_candi_company_ratio_top_semi_comp_0802_to_0801 = {}
DIC_candi_company_ratio_general_comp_0802_to_0801 = {}

median_ratio_top_semi_comp_0800_yesterday = 0
median_ratio_general_comp_0800_yesterday = 0

DIC_transaction_top_semi_comp_buy_target_quantity = {}
DIC_transaction_general_comp_buy_target_quantity = {}

DIC_candi_top_semi_company_transaction_money_0800_0801 = {}
DIC_candi_general_company_transaction_money_0800_0801 = {}

DIC_candi_top_semi_company_transaction_money_0800_0802 = {}
DIC_candi_general_company_transaction_money_0800_0802 = {}

DIC_transaction_top_semi_comp_buy_target_with_orderID = {}
DIC_transaction_general_comp_buy_target_with_orderID = {}

DIC_transaction_top_semi_comp_SELL_target_with_orderID = {}
DIC_transaction_general_comp_SELL_target_with_orderID = {}

DIC_top_semi_comp_bought_average_price = {}
DIC_general_comp_bought_average_price = {}

DIC_top_semi_comp_bought_quantity = {}
DIC_general_comp_bought_quantity = {}

total_bought_quantity = 0

market_condition = 99

#buy_state = 0

#bought_quantity_of_0 = 0
#bought_quantity_of_1 = 0

intermediate_price = 0

order_response = 0



'''
DIC_transaction_buy_target_with_company_name = {}
DIC_transaction_buy_target_with_price = {}
DIC_transaction_buy_target_with_quantity = {}


DIC_transaction_sell_target_with_volume = {}
DIC_transaction_sell_target_with_orderID = {}

DIC_candi_company_ratio_today_0801_to_0800 = {}
DIC_candi_company_buyable_price = {}
'''



while True:
    
    try:

        now = datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600))  # 클라우드 서버와 한국과의 시간차이 보정 (9시간)

        print ("now : ", now)

        # 7시에 토근 발행, 8시부터 거래 시작
        
        if ((7 <= now.hour < 8) and (50 <= now.minute < 51) and (0 <= now.second < (cycle_period + 1))) :   # (original values) ((7 <= now.hour < 8) and (50 <= now.minute < 51) and (0 <= now.second < (cycle_period + 1)))
            print ("[ Get transaction TOKEN ]\n")
            token_get = get_access_token(TOSS_CLIENT_ID, TOSS_CLIENT_SECRET)
            time.sleep(1)


            # ==========================================
            # [단계] 발급받은 진짜 토큰으로 계좌 조회하기
            # ==========================================

            print ("[ Current_ACCOUNT check ]")
            account_url = "https://openapi.tossinvest.com/api/v1/accounts"
            account_headers = {
                "Authorization": f"Bearer {token_get}"
                }

            account_response = requests.get(account_url, headers = account_headers)
            print(json.dumps(account_response.json(), indent=4, ensure_ascii=False))

            print ("\n[ Current Asset check ]\n")
            get_asset_check = asset_check(token_get)
            print ("\nget_asset_check :\n", get_asset_check)
            #print ("Currnt time : ", now)

            total_cash_buyable_today = get_toss_cash_buyable (token_get)
            #money_for_buy_a_item = total_cash_buyable_today // money_for_a_item_divider
            print("total_cash_buyable : {0:,} won".format (total_cash_buyable_today))

            cycle_in_transation_mode = 0.5
            hour_check = (datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600))).hour
            

            while ((datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600))).hour <= (hour_check + 1)) :
                
                now_in_mode = datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600))  # 클라우드 서버와 한국과의 시간차이 보정 (9시간)
                print ("[ Begin transaction mode at ] ", now_in_mode)
                               
                if ((7 <= now_in_mode.hour < 8) and (55 <= now_in_mode.minute < 56) and (0 <= now_in_mode.second < (cycle_in_transation_mode + 1))) :   # (original)  ((7 <= now_in_mode.hour < 8) and (55 <= now_in_mode.minute < 56) and (0 <= now_in_mode.second < (cycle_in_transation_mode + 1)))
                    print ("\n[ Get information YESTERDAY ending price at ] ", datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600)))

                    for i_stat_yesterday_ts in DIC_candi_top_semi_company.keys() :
                        print ("\n[ Get_1m_stat_Top_semi_company ] {0} : {1}".format(i_stat_yesterday_ts, DIC_candi_top_semi_company[i_stat_yesterday_ts]))
                        DF_1m_stat_yesterday_top_semi = get_1m_1d_candles(token_get, "1m", i_stat_yesterday_ts, 350, 200)
                        DF_1m_stat_yesterday_top_semi.index = DF_1m_stat_yesterday_top_semi.index.tz_localize(None)   # 타임존(+9:00) 제거
                        print (DF_1m_stat_yesterday_top_semi)
                        #DF_1m_stat_yesterday.to_excel("stat_1m_{0}.xlsx".format(DIC_candi_company[list(DIC_candi_company.keys())[i_stat_yesterday]]))
                        yesterday_end_value = DF_1m_stat_yesterday_top_semi.loc[DF_1m_stat_yesterday_top_semi.index.astype(str).str.contains("15:30:00"), "종가"].iloc[0]
                        print ("  Yesterday_end_price : {0} ".format(yesterday_end_value))
                        DIC_candi_top_semi_company_yesterday_end_price[i_stat_yesterday_ts] = int(yesterday_end_value)
                        time.sleep(0.5)

                    print ("\nDIC_candi_top_semi_company_yesterday_end_price :\n", DIC_candi_top_semi_company_yesterday_end_price)

                    

                    for i_stat_yesterday_general in DIC_candi_general_company.keys() :
                        print ("\n[ Get_1m_stat_general_company ] {0} : {1}".format(i_stat_yesterday_general, DIC_candi_general_company[i_stat_yesterday_general]))
                        DF_1m_stat_yesterday_general = get_1m_1d_candles(token_get, "1m", i_stat_yesterday_general, 350, 200)
                        DF_1m_stat_yesterday_general.index = DF_1m_stat_yesterday_general.index.tz_localize(None)   # 타임존(+9:00) 제거
                        print (DF_1m_stat_yesterday_general)
                        #DF_1m_stat_yesterday.to_excel("stat_1m_{0}.xlsx".format(DIC_candi_company[list(DIC_candi_company.keys())[i_stat_yesterday]]))
                        yesterday_end_value_general = DF_1m_stat_yesterday_general.loc[DF_1m_stat_yesterday_general.index.astype(str).str.contains("15:30:00"), "종가"].iloc[0]
                        print ("  Yesterday_end_price : {0} ".format(yesterday_end_value_general))
                        DIC_candi_general_company_yesterday_end_price[i_stat_yesterday_general] = int(yesterday_end_value_general)
                        time.sleep(0.5)

                    print ("\nDIC_candi_general_company_yesterday_end_price :\n", DIC_candi_general_company_yesterday_end_price)

                    print ("[ FINISH Getting information of YESTERDAY ending price at ]", datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600)))

                    

                elif ((market_condition != 0) and (8 <= now_in_mode.hour < 9) and (0 <= now_in_mode.minute < 1) and (0.5 <= now_in_mode.second < (1 + cycle_in_transation_mode + 1))) :   # (original) ((8 <= now_in_mode.hour < 9) and (0 <= now_in_mode.minute < 1) and (1 <= now_in_mode.second < (1 + cycle_in_transation_mode + 1)))
                    today_now = datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600))
                    today = str(today_now.strftime("%Y-%m-%d"))
                    #today = "2026-07-24"
                    print ("today is : ", today)
                    
                    print ("\n[ Get information Top_semi_comnay TODAY an starting price at ] ", today_now)

                    for i_stat_today_start in DIC_candi_top_semi_company.keys() :
                        print ("\n[ Get_1d_stat_Top_semi ] {0} : {1}".format(i_stat_today_start, DIC_candi_top_semi_company[i_stat_today_start]))
                        DF_1d_stat_today_start = get_1m_1d_candles(token_get, "1d", i_stat_today_start, 1, 2)
                        DF_1d_stat_today_start.index = DF_1d_stat_today_start.index.tz_localize(None)   # 타임존(+9:00) 제거
                        print (DF_1d_stat_today_start)
                        #DF_1d_stat_today_start.to_excel("stat_1d_{0}.xlsx".format(DIC_candi_company[list(DIC_candi_company.keys())[i_stat_today_start]]))
                        #today_start_value = DF_1d_stat_today_start.loc[DF_1d_stat_today_start.index.astype(str).str.contains(today), "시가"].iloc[0]
                        today_start_value = DF_1d_stat_today_start.loc[DF_1d_stat_today_start.index.astype(str).str.contains(today), "시가"].iloc[0]
                        print ("  Today_start_value : ", today_start_value)
                        DIC_candi_top_semi_company_0800_start_price[i_stat_today_start] = int(today_start_value)

                        ratio_today_yesterday = today_start_value / DIC_candi_top_semi_company_yesterday_end_price[i_stat_today_start]
                        print ("  ratio TODAY_start_price to YESTERDAY_end_price : ", ratio_today_yesterday)
                        DIC_candi_company_ratio_top_semi_comp_0800_to_yesterday[i_stat_today_start] = ratio_today_yesterday

                        transaction_money = today_start_value * DF_1d_stat_today_start.loc[DF_1d_stat_today_start.index.astype(str).str.contains(today), "거래량"].iloc[0]
                        print("  transaction_money_during_0800_to_until Now : {0:,}".format(transaction_money))
                        DIC_candi_top_semi_company_transaction_money_0800_0801[i_stat_today_start] = int(transaction_money)
                        time.sleep(0.1)

                    print ("\nratio TOP_Semi_company_TODAY_start_price to YESTERDAY_end_price\n", DIC_candi_company_ratio_top_semi_comp_0800_to_yesterday)
                    
                    median_ratio_top_semi_comp_0800_yesterday = statistics.median(list(DIC_candi_company_ratio_top_semi_comp_0800_to_yesterday.values()))
                    print ("\n [median_ratio]_of_TOP_semi_candidate_companies : ", median_ratio_top_semi_comp_0800_yesterday)

                    if ((list(DIC_candi_company_ratio_top_semi_comp_0800_to_yesterday.values())[0] >= 1.005) and (list(DIC_candi_company_ratio_top_semi_comp_0800_to_yesterday.values())[1] >= 1.002)) or \
                    ((list(DIC_candi_company_ratio_top_semi_comp_0800_to_yesterday.values())[0] >= 1.002) and (list(DIC_candi_company_ratio_top_semi_comp_0800_to_yesterday.values())[1] >= 1.005)) :
                        market_condition = 0
                        print ("Today's market_condition is 0")

                    else :
                        market_condition = 99
                        print ("Today's market_condition is NOT 0 and more check is needded to confirm market condition") 

                    print ("\n\nCurrent time_after setting market_condition_mode : ", (datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600))))
                    


                # market_condition = 0 일때, 08:00에 Top_semi 업체 매수
                if ((market_condition == 0) and (8 <= now_in_mode.hour < 9) and (0 <= now_in_mode.minute < 1) and (0.5 <= now_in_mode.second < 39)) :   # (original) ((market_condition == 0) and (8 <= now_in_mode.hour < 9) and (0 <= now_in_mode.minute < 1) and (2 <= now_in_mode.second < 60))
                    print ("[ Gettting start BUY transaction with market_condition # 0 of TOP Semi company at ]", datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600)))

                    

                    money_for_buy_a_top_semi_comp = total_cash_buyable_today // money_for_a_item_divider_for_top_semi_comp
                    print ("default money amount for a item : {0:,}".format(money_for_buy_a_top_semi_comp))

                    for i_target_buy in DIC_candi_top_semi_company.keys() :
                        print("\n{0}_{1} check : ".format(i_target_buy, DIC_candi_top_semi_company[i_target_buy]))
                        start_price = DIC_candi_top_semi_company_0800_start_price[i_target_buy]
                        try_to_buy_price, try_to_buy_volume = buyable_price_volume_with_unit(start_price, money_for_buy_a_top_semi_comp)

                        DIC_transaction_top_semi_comp_buy_target_quantity[i_target_buy] = try_to_buy_volume
                        print ("start_prince : {0:,} and buyable quantity : {1:,}".format(start_price, try_to_buy_volume))
                        time.sleep(0.1)


                    now_under_0801 = datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600))
                    #buy_trial_0800_top_semi = 0
                    #while (((now_under_0801.minute < 1) and (bought_quantity_of_0 < (2 * list(DIC_transaction_top_semi_comp_buy_target_quantity.values())[0]))) or ((now_under_0801.minute < 1) and (bought_quantity_of_1 < (2 * list(DIC_transaction_top_semi_comp_buy_target_quantity.values())[1])))) :
                    while ((8 <= now_under_0801.hour < 9) and (now_under_0801.minute < 1) and (now_under_0801.second < 39)) :

                        print ("now_under_0801_buy_transaction : ", datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600)))
                        
                        for i_buy_top_semi in DIC_candi_top_semi_company.keys() :
                            print("\n{0}_{1} check : ".format(i_buy_top_semi, DIC_candi_top_semi_company[i_buy_top_semi]))

                            bought_quantity = get_sellable_quantity(token_get, i_buy_top_semi)
                            print("   currently bought quantity : ", bought_quantity)

                            budget_buyable_now = get_toss_cash_buyable (token_get)

                            start_price_today = int(DIC_candi_top_semi_company_0800_start_price[i_buy_top_semi])
                            buy_trial_quantity_default = int(DIC_transaction_top_semi_comp_buy_target_quantity[i_buy_top_semi])
                            buy_trial_quantity_current_budget = budget_buyable_now // start_price_today
                            buy_trial_quantity_real = min(buy_trial_quantity_default, buy_trial_quantity_current_budget)
                            
                            print ("   buy check for start_price {0} and target_price {1} and volume {2}".format(start_price_today, start_price_today, buy_trial_quantity_real))

                            get_callable_ask_bid_price_info = get_orderbook(token_get, i_buy_top_semi) # 해당 주식의 매도/매수 호가 및 연관 물량 조회
                            
                            # 1. result 내부의 asks 배열 안전하게 접근
                            #asks_list = get_callable_ask_bid_price_info.get("result", {}).get("asks", [])
                            asks_list = get_callable_ask_bid_price_info.get("asks", [])
                            print("\n   asks price information : ", asks_list)

                            '''
                            # 2. 데이터 유무 확인 후 min()으로 최저가 추출
                            if asks_list :
                                callable_ask_price_0 = min(int(ask["price"]) for ask in asks_list)
                            
                            else:
                                callable_ask_price_0 = None
                                print("매도 호가 데이터가 존재하지 않습니다.")

                            '''
                            if asks_list :
                                callable_ask_price_0 = min(int(ask["price"]) for ask in asks_list)
                            else :
                                callable_ask_price_0 = None
                                print("매도 호가 데이터가 존재하지 않습니다.")

                            print ("   현재 매수할 수 있는 가격 : {0:,}".format(callable_ask_price_0))

                            if (len(asks_list) != 0) and (buy_trial_quantity_real != 0) and (DIC_transaction_top_semi_comp_buy_target_quantity[i_buy_top_semi] >= 1) and (callable_ask_price_0 <= start_price_today) :
                                print ("   Try to buy volume {0:,} with price less or equal than {1:,}".format (buy_trial_quantity_real, start_price_today))
                                order_response_0, orderID_buy_0 = run_toss_stock_buyer_seller (token_get, str(i_buy_top_semi), "BUY", "LIMIT", buy_trial_quantity_real, start_price_today)

                                if (order_response_0 == 1) :
                                    DIC_transaction_top_semi_comp_buy_target_with_orderID[i_buy_top_semi] = orderID_buy_0
                            
                            time.sleep(0.1)

                        # 매수 안된 주문은 취소하기
                        for i_buy_order_check in list(DIC_transaction_top_semi_comp_buy_target_with_orderID.keys()) :
                            print ("\n{0}_{1} transaction result check".format(i_buy_order_check, DIC_candi_top_semi_company[i_buy_order_check]))
                            check_result = transaction_result_check (token_get, DIC_transaction_top_semi_comp_buy_target_with_orderID[i_buy_order_check])
                            if (check_result != 1) :
                                print("All or partial {0}_{1} buy transaction order will be canceled".format (i_buy_order_check, DIC_candi_top_semi_company[i_buy_order_check]))
                                cancel_order = cancel_toss_stock_order(token_get, DIC_transaction_top_semi_comp_buy_target_with_orderID[i_buy_order_check])
                                DIC_transaction_top_semi_comp_buy_target_with_orderID.pop(i_buy_order_check, None)   # 취소한 orderID는 삭제
                            time.sleep(0.1)


                        now_under_0801 = datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600))
                        #bought_quantity_of_0 = get_sellable_quantity(token_get, str(list(DIC_candi_top_semi_company.keys())[0]))
                        #bought_quantity_of_1 = get_sellable_quantity(token_get, str(list(DIC_candi_top_semi_company.keys())[1]))
                        #time.sleep(0.5)

                        print ("\n0800 to 0801 buy cycle : ", now_under_0801)
                        print ("buy_quantitly of {0}_{1} is target {2}  / bought {3}".format(list(DIC_candi_top_semi_company.keys())[0], list(DIC_candi_top_semi_company.values())[0], list(DIC_transaction_top_semi_comp_buy_target_quantity.values())[0], get_sellable_quantity(token_get, list(DIC_candi_top_semi_company.keys())[0])))
                        #time.sleep(0.1)
                        print ("buy_quantitly of {0}_{1} is target {2}  / bought {3}".format(list(DIC_candi_top_semi_company.keys())[1], list(DIC_candi_top_semi_company.values())[1], list(DIC_transaction_top_semi_comp_buy_target_quantity.values())[1], get_sellable_quantity(token_get, list(DIC_candi_top_semi_company.keys())[1])))

                        #time.sleep(0.1)

                # market_condition = 0 일때, 08:00:30 즈음에 general company의 median 추출하기
                elif ((market_condition == 0) and (8 <= now_in_mode.hour < 9) and (0 <= now_in_mode.minute < 1) and (39 <= now_in_mode.second < 47)) :
                    print ("[ Gettting gathering # 0 of General company at ] ", datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600)))


                    for i_stat_today_start_general in DIC_candi_general_company.keys() :
                        print ("\n[ Get_1d_stat_general_comp ] {0} : {1}".format(i_stat_today_start_general, DIC_candi_general_company[i_stat_today_start_general]))
                        DF_1d_stat_today_start_general = get_1m_1d_candles(token_get, "1d", i_stat_today_start_general, 1, 2)
                        DF_1d_stat_today_start_general.index = DF_1d_stat_today_start_general.index.tz_localize(None)   # 타임존(+9:00) 제거
                        print (DF_1d_stat_today_start_general)
                        today_start_value_general = DF_1d_stat_today_start_general.loc[DF_1d_stat_today_start_general.index.astype(str).str.contains(today), "시가"].iloc[0]
                        print ("  Today_start_value : ", today_start_value_general)
                        DIC_candi_general_company_0800_start_price[i_stat_today_start_general] = int(today_start_value_general)

                        ratio_today_yesterday_general = today_start_value_general / DIC_candi_general_company_yesterday_end_price[i_stat_today_start_general]
                        print ("  ratio TODAY_start_price to YESTERDAY_end_price : ", ratio_today_yesterday_general)
                        DIC_candi_company_ratio_general_comp_0800_to_yesterday[i_stat_today_start_general] = ratio_today_yesterday_general
                        time.sleep(0.1)

                    print ("\nratio General_company_TODAY_start_price to YESTERDAY_end_price\n", DIC_candi_company_ratio_general_comp_0800_to_yesterday)
                    
                    median_ratio_general_comp_0800_yesterday = statistics.median(list(DIC_candi_company_ratio_general_comp_0800_to_yesterday.values()))
                    print ("\n [median_ratio]_of_general_candidate_companies : ", median_ratio_general_comp_0800_yesterday)


                # market_condition = 0 일때, 만약 median of general company at 0800이 좋지 않다면, 0801에 top_semi 매도
                elif ((market_condition == 0) and (8 <= now_in_mode.hour < 9) and (1 <= now_in_mode.minute < 2) and (0 <= now_in_mode.second < 2)) :

                    bought_quantity_top_semi_A = 0
                    bought_quantity_top_semi_B = 0                                              
                    bought_quantity_top_semi_A = get_sellable_quantity(token_get, list(DIC_candi_top_semi_company.keys())[0])
                    bought_quantity_top_semi_B = get_sellable_quantity(token_get, list(DIC_candi_top_semi_company.keys())[1])
                    
                    if ((bought_quantity_top_semi_A + bought_quantity_top_semi_B) >= 1) and (median_ratio_general_comp_0800_yesterday != 0) and ((median_ratio_general_comp_0800_yesterday < 1) or ((median_ratio_general_comp_0800_yesterday < 1.005) and ((median_ratio_top_semi_comp_0800_yesterday - median_ratio_general_comp_0800_yesterday) >= 0.035))) :
                        print ("   \n\n\nEarly Sell transaction conducting with market condition 0 at : ",  (datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600))))

                        for i_sell_top_semi_early in DIC_candi_top_semi_company.keys() :
                            try_to_sell_quantity_early = get_sellable_quantity(token_get, i_sell_top_semi_early)                       
                            print ("{0}_{1} is under checking of selling of TOP SEMI companies with quantity of {2:,}".format(i_sell_top_semi_early, DIC_candi_top_semi_company[i_sell_top_semi_early], int(try_to_sell_quantity_early)))                        
    
                            get_callable_ask_bid_price_info_sell_early = get_orderbook(token_get, str(i_sell_top_semi_early)) # 해당 주식의 매도/매수 호가 및 연관 물량 조회
    
                            # 1. result 내부의 bids 배열 안전하게 접근
                            bids_list_early = get_callable_ask_bid_price_info_sell_early.get("bids", [])
                            print("bids price information : ", bids_list_early)
    
                            # 2. 데이터 유무 확인 후 max()으로 최고가 추출
                            if bids_list_early :
                                callable_bid_price_0_early = max(int(bid["price"]) for bid in bids_list_early)
                            
                            else :
                                callable_bid_price_0_early = None
                                print("매수 호가 데이터가 존재하지 않습니다.")                       
                            #callable_bid_price_0 = int(get_callable_ask_bid_price_info_sell["bids"][0]["price"])   # 현재 첫번째로 높은 매수 호가 (현재 해당 주식을 어떤 사람이 사겠다고 제안한 가격)
    
                            if (callable_bid_price_0_early is not None) :
                                order_response_sell_early, orderID_sell_early = run_toss_stock_buyer_seller(token_get, str(i_sell_top_semi_early), "SELL", "LIMIT", try_to_sell_quantity_early, callable_bid_price_0_early)
                                time.sleep(0.5)
                                sellable_quantity_after_order_early = get_sellable_quantity(token_get, str(i_sell_top_semi_early))
                                print ("\n{0}_{1} bought quantity after sell order is {2:,}".format(i_sell_top_semi_early, DIC_candi_top_semi_company[i_sell_top_semi_early], int(sellable_quantity_after_order_early)))
                                
                                if (order_response_sell_early == 1) :
                                    DIC_transaction_top_semi_comp_SELL_target_with_orderID[i_sell_top_semi_early] = orderID_sell_early
                                    print ("orderID_sell_early : ", orderID_sell_early)                                
                            time.sleep(0.1)
                            print("DIC_transaction_top_semi_comp_SELL_target_with_orderID :\n", DIC_transaction_top_semi_comp_SELL_target_with_orderID)
                            
    
                        # 매도 안된 주문은 취소하기
                        for i_sell_check_early in list(DIC_transaction_top_semi_comp_SELL_target_with_orderID.keys()) :
                            sellable_quantity_current_early = get_sellable_quantity(token_get, str(i_sell_check_early))
    
                            if (sellable_quantity_current_early >= 1) :
                                print("UnSold quantity order is cenceled of {0}_{1} with quantity {2:,}".format(i_sell_check_early, DIC_candi_top_semi_company[i_sell_check_early], int(sellable_quantity_current_early)))
                                cancel_order = cancel_toss_stock_order(token_get, DIC_transaction_top_semi_comp_SELL_target_with_orderID[i_sell_check_early])
                                DIC_transaction_top_semi_comp_SELL_target_with_orderID.pop(i_sell_check_early, None)   # 취소한 orderID는 삭제
                            time.sleep(0.1)
    
                        time.sleep(0.1)



                # market_condition = 0 일때, 08:01에 general 업체 매수
                elif ((market_condition == 0) and (8 <= now_in_mode.hour < 9) and (1 <= now_in_mode.minute < 2) and (2 <= now_in_mode.second < 60)) :   # (original) ((market_condition == 0) and (8 <= now_in_mode.hour < 9) and (1 <= now_in_mode.minute < 2) and (2 <= now_in_mode.second < 60))
                    print ("[ Gettting start BUY transaction with market_condition # 0 of General company at ]", datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600)))

                    total_cash_buyable_residual = get_toss_cash_buyable (token_get)

                    money_for_buy_a_general_comp = total_cash_buyable_residual // money_for_a_item_divider_for_general_comp

                    for i_stat_1m in DIC_candi_general_company.keys() :
                        print ("\n[ Get_1m_stat ] {0} : {1}".format(i_stat_1m, DIC_candi_general_company[i_stat_1m]))
                        DF_1m_stat = get_1m_1d_candles(token_get, "1m", i_stat_1m, 1, 5)
                        DF_1m_stat.index = DF_1m_stat.index.tz_localize(None)   # 타임존(+9:00) 제거
                        #print ("[ Get_1m_stat ] {0} : {1}".format(i_stat_1m, i_stat_1m, DIC_candi_general_company[i_stat_1m]))
                        #DF_1m_stat.to_excel("stat_1m_{0}.xlsx".format(DIC_candi_company[list(DIC_candi_company.keys())[i_stat_1m]]))
                        start_price_0800 = DF_1m_stat.loc[DF_1m_stat.index.astype(str).str.contains("08:01:00"), "시가"].iloc[0]
                        start_price_0801 = DF_1m_stat.loc[DF_1m_stat.index.astype(str).str.contains("08:01:00"), "종가"].iloc[0]
                        # (for test) today_start_value = DF_1m_stat.loc[DF_1m_stat.index.astype(str).str.contains("20:00:00"), "시가"].iloc[0]
                        ratio_0801_start_price_to_0800_start_price = start_price_0801 / start_price_0800
                        print ("start_price_0801 : {0:,}, start_price_0800 : {1:,} ___ ratio : {2}".format (start_price_0801, start_price_0800, ratio_0801_start_price_to_0800_start_price))
                        DIC_candi_general_company_0800_start_price[i_stat_1m] = int(start_price_0800)
                        DIC_candi_general_company_0801_start_price[i_stat_1m] = int(start_price_0801)
                        DIC_candi_company_ratio_general_comp_0801_to_0800[i_stat_1m] = float(ratio_0801_start_price_to_0800_start_price)
                        
                        try_to_buy_price_s, try_to_buy_volume_s = buyable_price_volume_with_unit(start_price_0800, money_for_buy_a_general_comp)
                        DIC_transaction_general_comp_buy_target_quantity[i_stat_1m] = try_to_buy_volume_s

                        transaction_money_0800_0801 = DF_1m_stat.loc[DF_1m_stat.index.astype(str).str.contains("08:01:00"), "종가"].iloc[0] * DF_1m_stat.loc[DF_1m_stat.index.astype(str).str.contains('08:01:00'), "거래량"].iloc[0]
                        print("transaction_money_during_0800_0801 : {0:,}".format(transaction_money_0800_0801))
                        DIC_candi_general_company_transaction_money_0800_0801[i_stat_1m] = int(transaction_money_0800_0801)
                        time.sleep(0.1)

                    print ("\n\nDIC_candi_general_company_ratio_today_0801_to_0800 : \n", DIC_candi_company_ratio_general_comp_0801_to_0800)
                    print ("\nDIC_candi_general_company_transaction_money_0800_to_0801 : \n", DIC_candi_general_company_transaction_money_0800_0801)


                    now_under_0802 = datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600))
                    print ("Now before 0801~0802 buy transaction : ", now_under_0802)
                    while ((datetime.datetime.now()).minute < 2) :

                        for i_screening_buy_item in DIC_candi_general_company.keys() :
                            
                            print("\n{0}_{1} check : try_to_buy_quantity {2:,}_is bigger than or equal to? 1 AND transaction_money from today start {3:,} _is bigger than or equal to?_ {4:,} AND ratio_0801_to_0800 {5} _is lower than_ {6}".\
                                  format(i_screening_buy_item, DIC_candi_general_company[i_screening_buy_item], int(DIC_transaction_general_comp_buy_target_quantity[i_screening_buy_item]), \
                                         int(DIC_candi_general_company_transaction_money_0800_0801[i_screening_buy_item]), int(transaction_money_criteria), \
                                         DIC_candi_company_ratio_general_comp_0801_to_0800[i_screening_buy_item], ratio_0801_to_0800_price_check_criteria))
    
                            if (DIC_transaction_general_comp_buy_target_quantity[i_screening_buy_item] >= 1) and (DIC_candi_general_company_transaction_money_0800_0801[i_screening_buy_item] >= transaction_money_criteria) and (DIC_candi_company_ratio_general_comp_0801_to_0800[i_screening_buy_item] <= ratio_0801_to_0800_price_check_criteria) :
                                get_callable_ask_bid_price_info_s = get_orderbook(token_get, i_screening_buy_item) # 해당 주식의 매도/매수 호가 및 연관 물량 조회
                                
                                # 1. result 내부의 asks 배열 안전하게 접근
                                asks_list_s = get_callable_ask_bid_price_info_s.get("asks", [])
                                print("asks price information : ", asks_list_s)

                                # 2. 데이터 유무 확인 후 min()으로 최저가 추출
                                if asks_list_s :
                                    callable_ask_price_0_s = min(int(ask["price"]) for ask in asks_list_s)
                                else :
                                    callable_ask_price_0_s = None
                                    print("매도 호가 데이터가 존재하지 않습니다.")
                                
                                #callable_ask_price_0_s = int(get_callable_ask_bid_price_info_s["asks"][0]["price"])   # 현재 가장 낮은 매도 호가 (현재 해당 주식을 갖고 있는 사람이 팔겠다고 제안한 가격)
                                print ("   현재 매수할 수 있는 가격 : {0:,}".format(callable_ask_price_0_s))
                                if (callable_ask_price_0_s is not None) and (callable_ask_price_0_s <= (ratio_0801_to_0800_price_buy_criteria * DIC_candi_general_company_0800_start_price[i_screening_buy_item])) :
                                    print ("   Try to buy volume {0:,} with price {1:,}".format (DIC_transaction_general_comp_buy_target_quantity[i_screening_buy_item], callable_ask_price_0_s))
                                    order_response_b_s, orderID_buy_b_s = run_toss_stock_buyer_seller (token_get, str(i_screening_buy_item), "BUY", "LIMIT", DIC_transaction_general_comp_buy_target_quantity[i_screening_buy_item], callable_ask_price_0_s)
    
                                    if (order_response_b_s == 1) :
                                        DIC_transaction_general_comp_buy_target_with_orderID[i_screening_buy_item] = orderID_buy_b_s
                            time.sleep(0.1)
                            
    
                        for i_buy_order_check_s in list(DIC_transaction_general_comp_buy_target_with_orderID.keys()) :
                            check_result_s = transaction_result_check (token_get, DIC_transaction_general_comp_buy_target_with_orderID[i_buy_order_check_s])
                            if (check_result_s != 1) :
                                print("All or partial {0}_{1} buy transaction order is canceled".format (i_buy_order_check_s, DIC_candi_general_company[i_buy_order_check_s]))
                                cancel_order = cancel_toss_stock_order(token_get, DIC_transaction_general_comp_buy_target_with_orderID[i_buy_order_check_s])
                                DIC_transaction_general_comp_buy_target_with_orderID.pop(i_buy_order_check, None)   # 취소한 orderID는 삭제
                            time.sleep(0.1)

                        now_under_0802 = datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600))

                        time.sleep(0.5)
                        print ("Now under 0801~0802 buy transaction : ", now_under_0802)

                        

                # market_condition = 0이 아닐때, 08:02에 market 상태 점검
                elif ((market_condition != 0) and (8 <= now_in_mode.hour < 9) and (2 <= now_in_mode.minute < 3) and (1 <= now_in_mode.second < 60)) :   # (original) ((market_condition == 0) and (8 <= now_in_mode.hour < 9) and (1 <= now_in_mode.minute < 2) and (2 <= now_in_mode.second < 60))
                    print ("[ Checking Market condition in case of market condition is NOT #0 at ]", datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600)))

                    total_cash_buyable_residual_s = get_toss_cash_buyable (token_get)

                    money_for_buy_a_general_comp_s = total_cash_buyable_residual_s // money_for_a_item_divider_for_general_comp

                    print ("money_for_buy_a_general_comp : {0:,}".format(money_for_buy_a_general_comp_s))

                    print ("\n  Checking Top Semi company market condition")


                    for i_stat_yesterday_ts_s in DIC_candi_top_semi_company.keys() :
                        print ("\n[ Get_1m_stat_Top_semi_company ] {0} : {1}".format(i_stat_yesterday_ts_s, DIC_candi_top_semi_company[i_stat_yesterday_ts_s]))
                        DF_1m_stat_yesterday_top_semi = get_1m_1d_candles(token_get, "1m", i_stat_yesterday_ts_s, 1, 5)
                        DF_1m_stat_yesterday_top_semi.index = DF_1m_stat_yesterday_top_semi.index.tz_localize(None)   # 타임존(+9:00) 제거
                        print (DF_1m_stat_yesterday_top_semi)
                        #DF_1m_stat_yesterday.to_excel("stat_1m_{0}.xlsx".format(DIC_candi_company[list(DIC_candi_company.keys())[i_stat_yesterday]]))
                        yesterday_end_value_top_semi_comp = DIC_candi_top_semi_company_yesterday_end_price[i_stat_yesterday_ts_s]
                        start_price_0800_top_semi_comp = DF_1m_stat_yesterday_top_semi.loc[DF_1m_stat_yesterday_top_semi.index.astype(str).str.contains("08:01:00"), "시가"].iloc[0]
                        start_price_0801_top_semi_comp = DF_1m_stat_yesterday_top_semi.loc[DF_1m_stat_yesterday_top_semi.index.astype(str).str.contains("08:02:00"), "시가"].iloc[0]
                        start_price_0802_top_semi_comp = DF_1m_stat_yesterday_top_semi.loc[DF_1m_stat_yesterday_top_semi.index.astype(str).str.contains("08:02:00"), "종가"].iloc[0]
                        # (for test) today_start_value = DF_1m_stat_yesterday_top_semi.loc[DF_1m_stat_yesterday_top_semi.index.astype(str).str.contains("20:00:00"), "시가"].iloc[0]
                        ratio_0802_start_price_to_yesterday_price_top_semi_comp = start_price_0802_top_semi_comp / yesterday_end_value_top_semi_comp
                        DIC_candi_company_ratio_top_semi_comp_0802_to_yesterday[i_stat_yesterday_ts_s] = ratio_0802_start_price_to_yesterday_price_top_semi_comp
                        time.sleep(0.1)

                    median_0802_to_yesterday_top_semi_comp = statistics.median(list(DIC_candi_company_ratio_top_semi_comp_0802_to_yesterday.values()))
                    print ("median_0802_to_yesterday_top_semi_comp : ", median_0802_to_yesterday_top_semi_comp)

                    

                    for i_stat_yesterday_general_s in DIC_candi_general_company.keys() :
                        print ("\n[ Get_1m_stat_general_company ] {0} : {1}".format(i_stat_yesterday_general_s, DIC_candi_general_company[i_stat_yesterday_general_s]))
                        DF_1m_stat_yesterday_general_comp = get_1m_1d_candles(token_get, "1m", i_stat_yesterday_general_s, 1, 5)
                        DF_1m_stat_yesterday_general_comp.index = DF_1m_stat_yesterday_general_comp.index.tz_localize(None)   # 타임존(+9:00) 제거
                        print (DF_1m_stat_yesterday_general_comp)
                        #DF_1m_stat_yesterday.to_excel("stat_1m_{0}.xlsx".format(DIC_candi_company[list(DIC_candi_company.keys())[i_stat_yesterday]]))
                        yesterday_end_value_general_comp = DIC_candi_general_company_yesterday_end_price[i_stat_yesterday_general_s]
                        start_price_0800_general_comp = DF_1m_stat_yesterday_general_comp.loc[DF_1m_stat_yesterday_general_comp.index.astype(str).str.contains("08:01:00"), "시가"].iloc[0]
                        start_price_0801_general_comp = DF_1m_stat_yesterday_general_comp.loc[DF_1m_stat_yesterday_general_comp.index.astype(str).str.contains("08:02:00"), "시가"].iloc[0]
                        start_price_0802_general_comp = DF_1m_stat_yesterday_general_comp.loc[DF_1m_stat_yesterday_general_comp.index.astype(str).str.contains("08:02:00"), "종가"].iloc[0]
                        # (for test) today_start_value = DF_1m_stat_yesterday_general_comp.loc[DF_1m_stat_yesterday_general_comp.index.astype(str).str.contains("20:00:00"), "시가"].iloc[0]
                        ratio_0800_start_price_to_yesterday_price_general_comp = start_price_0800_general_comp / yesterday_end_value_general_comp
                        ratio_0801_start_price_to_yesterday_price_general_comp = start_price_0801_general_comp / yesterday_end_value_general_comp 
                        ratio_0802_start_price_to_yesterday_price_general_comp = start_price_0802_general_comp / yesterday_end_value_general_comp
                        #ratio_0802_start_price_to_0801_start_price_general_comp = start_price_0802_general_comp / start_price_0801_general_comp
                        DIC_candi_general_company_0800_start_price[i_stat_yesterday_general_s] = start_price_0800_general_comp
                        DIC_candi_company_ratio_general_comp_0800_to_yesterday[i_stat_yesterday_general_s] = ratio_0800_start_price_to_yesterday_price_general_comp                          
                        DIC_candi_company_ratio_general_comp_0801_to_yesterday[i_stat_yesterday_general_s] = ratio_0801_start_price_to_yesterday_price_general_comp                        
                        DIC_candi_company_ratio_general_comp_0802_to_yesterday[i_stat_yesterday_general_s] = ratio_0802_start_price_to_yesterday_price_general_comp

                        try_to_buy_price_t, try_to_buy_volume_t = buyable_price_volume_with_unit(start_price_0800_general_comp, money_for_buy_a_general_comp_s)
                        DIC_transaction_general_comp_buy_target_quantity[i_stat_yesterday_general_s] = try_to_buy_volume_t
                        #DIC_candi_company_ratio_general_comp_0802_to_0801[i_stat_yesterday_general_s] = ratio_0802_start_price_to_0801_start_price_general_comp
                        
                        transaction_money_0800_0802 = (DF_1m_stat_yesterday_general_comp.loc[DF_1m_stat_yesterday_general_comp.index.astype(str).str.contains("08:01:00"), "종가"].iloc[0] * DF_1m_stat_yesterday_general_comp.loc[DF_1m_stat_yesterday_general_comp.index.astype(str).str.contains('08:01:00'), "거래량"].iloc[0]) + (DF_1m_stat_yesterday_general_comp.loc[DF_1m_stat_yesterday_general_comp.index.astype(str).str.contains("08:02:00"), "종가"].iloc[0] * DF_1m_stat_yesterday_general_comp.loc[DF_1m_stat_yesterday_general_comp.index.astype(str).str.contains('08:02:00'), "거래량"].iloc[0])
                        print("transaction_money_during_0800_0802 : {0:,}".format(transaction_money_0800_0802))
                        DIC_candi_general_company_transaction_money_0800_0802[i_stat_yesterday_general_s] = int(transaction_money_0800_0802)
                        
                        time.sleep(0.1)

                    median_0801_to_yesterday_general_comp = statistics.median(list(DIC_candi_company_ratio_general_comp_0801_to_yesterday.values()))
                    median_0802_to_yesterday_general_comp = statistics.median(list(DIC_candi_company_ratio_general_comp_0802_to_yesterday.values()))

                    print ("median_0802_to_yesterday_top_semi_comp : {0},        median_0801_to_yesterday_general_comp : {1} _ median_0802_to_yesterday_general_comp : {2}".\
                           format(median_0802_to_yesterday_top_semi_comp, median_0801_to_yesterday_general_comp, median_0802_to_yesterday_general_comp))


                    while ((2 <= (datetime.datetime.now()).minute <= 3) and (median_0802_to_yesterday_top_semi_comp >= 0.97) and (median_0802_to_yesterday_general_comp >= 0.985) and (median_0802_to_yesterday_general_comp < median_0801_to_yesterday_general_comp)) :
                        
                        for i_buy_check_general_comp in DIC_candi_general_company.keys() :
                            print ("Buy condition Check of {0}_{1}\n".format(i_buy_check_general_comp, DIC_candi_general_company[i_buy_check_general_comp]))
                            if (DIC_candi_company_ratio_general_comp_0802_to_yesterday[i_buy_check_general_comp] < DIC_candi_company_ratio_general_comp_0801_to_yesterday[i_buy_check_general_comp]) and (DIC_candi_company_ratio_general_comp_0802_to_yesterday[i_buy_check_general_comp] < (DIC_candi_company_ratio_general_comp_0800_to_yesterday[i_buy_check_general_comp] - 0.005)) :
                                get_callable_ask_bid_price_info_t = get_orderbook(token_get, i_buy_check_general_comp) # 해당 주식의 매도/매수 호가 및 연관 물량 조회

                                # 1. result 내부의 asks 배열 안전하게 접근
                                asks_list_t = get_callable_ask_bid_price_info_t.get("asks", [])
                                print("asks price information : ", asks_list_t)

                                # 2. 데이터 유무 확인 후 min()으로 최저가 추출
                                if asks_list_t :
                                    callable_ask_price_0_t = min(int(ask["price"]) for ask in asks_list_t)
                                else :
                                    callable_ask_price_0_t = None
                                    print("매도 호가 데이터가 존재하지 않습니다.")
                                    
                                #callable_ask_price_0_t = int(get_callable_ask_bid_price_info_t["asks"][0]["price"])   # 현재 가장 낮은 매도 호가 (현재 해당 주식을 갖고 있는 사람이 팔겠다고 제안한 가격)
                                print ("   현재 매수할 수 있는 가격 : {0:,}".format(callable_ask_price_0_t))
                                if (callable_ask_price_0_t is not None) and (callable_ask_price_0_t <= (ratio_0801_to_0800_price_buy_criteria * DIC_candi_general_company_0800_start_price[i_buy_check_general_comp])) and (DIC_candi_general_company_transaction_money_0800_0802[i_buy_check_general_comp] > transaction_money_criteria) :
                                    print ("   Try to buy volume {0:,} with price {1:,}".format (DIC_transaction_general_comp_buy_target_quantity[i_buy_check_general_comp], callable_ask_price_0_t))
                                    order_response_b_t, orderID_buy_b_t = run_toss_stock_buyer_seller (token_get, str(i_buy_check_general_comp), "BUY", "LIMIT", DIC_transaction_general_comp_buy_target_quantity[i_buy_check_general_comp], callable_ask_price_0_t)
    
                                    if (order_response_b_t == 1) :
                                        DIC_transaction_general_comp_buy_target_with_orderID[i_buy_check_general_comp] = orderID_buy_b_t
                            time.sleep(0.1)

                        print ("DIC_transaction_general_comp_buy_target_with_orderID :", DIC_transaction_general_comp_buy_target_with_orderID)


                        for i_buy_order_check_t in list(DIC_transaction_general_comp_buy_target_with_orderID.keys()) :
                            check_result_t = transaction_result_check (token_get, DIC_transaction_general_comp_buy_target_with_orderID[i_buy_order_check_t])
                            if (check_result_t != 1) :
                                print("All or partial {0}_{1} buy transaction order is canceled".format (i_buy_order_check_t, DIC_candi_general_company[i_buy_order_check_t]))
                                cancel_order = cancel_toss_stock_order(token_get, DIC_transaction_general_comp_buy_target_with_orderID[i_buy_order_check_t])
                                DIC_transaction_general_comp_buy_target_with_orderID.pop(i_buy_order_check_t, None)   # 취소한 orderID는 삭제
                                
                            time.sleep(0.1)



                
                
                # [at 08:04]   market = 0 상황에서, 08:00에 매수한 종목의 average price를 추출하여 dictionary로 구성
                elif ((market_condition == 0) and (8 <= now_in_mode.hour < 9) and (4 <= now_in_mode.minute < 5) and (now_in_mode.second < 50)) :
                    asset_current = asset_check (token_get)
                    print ("current asset : \n ", asset_current)

                    for i_average_price in DIC_candi_top_semi_company.keys() :
                        items = asset_current.get("result", {}).get("items", [])
                        target_item = next((item for item in items if str(item.get("symbol")) == i_average_price), None)

                        bought_quantity_top_semi_comp = get_sellable_quantity(token_get, i_average_price)

                        print ("{0}_{1}_average bought price AND bought_quantity check".format(i_average_price, DIC_candi_top_semi_company[i_average_price]))

                        if target_item:
                            aver_price = target_item.get("averagePurchasePrice")
                            print("{0}_{1} : 평균매수가 {2:,} AND 매수 물량 {3:,}".format(i_average_price, DIC_candi_top_semi_company[i_average_price], aver_price, int(bought_quantity_top_semi_comp)))
                            DIC_top_semi_comp_bought_average_price[i_average_price] = aver_price
                            DIC_top_semi_comp_bought_quantity[i_average_price] = int(bought_quantity_top_semi_comp)

                        else:
                            print("해당 symbol을 찾을 수 없습니다.")
                        time.sleep(0.1)
                    print("\nDIC_top_semi_comp_bought_average_price : \n", DIC_top_semi_comp_bought_average_price)
                    print("DIC_top_semi_comp_bought_quantity : \n", DIC_top_semi_comp_bought_quantity)

                        

                    for i_average_price_g in DIC_candi_general_company.keys() :
                        items_g = asset_current.get("result", {}).get("items", [])
                        target_item_g = next((item for item in items_g if str(item.get("symbol")) == i_average_price_g), None)

                        bought_quantity_general_comp = get_sellable_quantity(token_get, i_average_price_g)
                        
                        print ("{0}_{1}_average bought price check".format(i_average_price_g, DIC_candi_general_company[i_average_price_g]))

                        if target_item_g:
                            aver_price_g = target_item_g.get("averagePurchasePrice")
                            print("{0}_{1} : 평균매수가 {2:,} AND 매수 물량 {3:,}".format(i_average_price_g, DIC_candi_general_company[i_average_price_g], aver_price_g, int(bought_quantity_general_comp)))
                            DIC_general_comp_bought_average_price[i_average_price_g] = aver_price_g
                            DIC_general_comp_bought_quantity[i_average_price_g] = int(bought_quantity_general_comp)

                        else:
                            print("해당 symbol을 찾을 수 없습니다.")
                        time.sleep(0.1)
                    print("\nDIC_general_comp_bought_average_price : \n", DIC_general_comp_bought_average_price)
                    print("DIC_general_comp_bought_quantity : \n", DIC_general_comp_bought_quantity)

                    total_bought_quantity = sum(DIC_top_semi_comp_bought_quantity.values()) + sum(DIC_general_comp_bought_quantity.values())
                    

                    time.sleep(10)

                
                # [from 08:05]   market = 0 상황에서, 08:00에 매수한 top semi 종목 매도
                elif (market_condition == 0) and (total_bought_quantity >= 1) and ((len(DIC_top_semi_comp_bought_average_price) + len(DIC_general_comp_bought_average_price)) >= 1) and (((8 <= now_in_mode.hour < 9) and (5 <= now_in_mode.minute <= 13)) or ((8 <= now_in_mode.hour < 9) and (14 <= now_in_mode.minute < 15) and (0 <= now_in_mode.second < 30)))  :
                    print ("   \n\n\nSell transaction conducting with market condition 0 at : ",  (datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600))))

                    for i_sell in DIC_top_semi_comp_bought_average_price.keys() :
                        try_to_sell_quantity = get_sellable_quantity(token_get, i_sell)
                        print ("{0}_{1} is under checking of selling of TOP SEMI companies with quantity : {2:,}".format(i_sell, DIC_candi_top_semi_company[i_sell], try_to_sell_quantity))

                        if (try_to_sell_quantity >= 1) :
                            print ("{0}_{1} is under checking of selling of TOP SEMI companies".format(i_sell, DIC_candi_top_semi_company[i_sell]))
                            bought_price = DIC_top_semi_comp_bought_average_price[i_sell]
                            yesterday_finished_price = DIC_candi_top_semi_company_yesterday_end_price[i_sell]
                            print ("average bought price is {0:,} and sellable quantity is {1:,}".format(bought_price, try_to_sell_quantity))
    
                            get_callable_ask_bid_price_info_sell = get_orderbook(token_get, str(i_sell)) # 해당 주식의 매도/매수 호가 및 연관 물량 조회
    
                            # 1. result 내부의 bids 배열 안전하게 접근
                            bids_list = get_callable_ask_bid_price_info_sell.get("bids", [])
                            print("bids price information : ", bids_list)
    
                            # 2. 데이터 유무 확인 후 min()으로 최저가 추출
                            if bids_list :
                                callable_bid_price_0 = max(int(bid["price"]) for bid in bids_list)
                            
                            else :
                                callable_bid_price_0 = None
                                print("매수 호가 데이터가 존재하지 않습니다.")                       
                            #callable_bid_price_0 = int(get_callable_ask_bid_price_info_sell["bids"][0]["price"])   # 현재 첫번째로 높은 매수 호가 (현재 해당 주식을 어떤 사람이 사겠다고 제안한 가격)
    
                            if (callable_bid_price_0 is not None) and (try_to_sell_quantity >= 1) and (callable_bid_price_0 >= (0.8 * yesterday_finished_price)) and ((callable_bid_price_0 > bought_price) or (callable_bid_price_0 <= (0.99 * bought_price))) :
                                order_response_sell, orderID_sell = run_toss_stock_buyer_seller(token_get, str(i_sell), "SELL", "LIMIT", try_to_sell_quantity, callable_bid_price_0)
                                time.sleep(0.5)
                                sellable_quantity_after_order = get_sellable_quantity(token_get, str(i_sell))
                                print ("\n{0}_{1} bought quantity after sell order is {2}".format(i_sell, DIC_candi_top_semi_company[i_sell], sellable_quantity_after_order))
                                
                                if (order_response_sell == 1) :
                                    DIC_transaction_top_semi_comp_SELL_target_with_orderID[i_sell] = orderID_sell
                                    print ("orderID_sell : ", orderID_sell)                                
                            time.sleep(0.1)
                            print("DIC_transaction_top_semi_comp_SELL_target_with_orderID :\n", DIC_transaction_top_semi_comp_SELL_target_with_orderID)
                        time.sleep(0.1)
                        

                    # 매도 안된 주문은 취소하기
                    for i_sell_check in list(DIC_transaction_top_semi_comp_SELL_target_with_orderID.keys()) :
                        sellable_quantity_current = get_sellable_quantity(token_get, str(i_sell_check))

                        if (sellable_quantity_current >= 1) :
                            print("UnSold quantity order is cenceled of {0}_{1} with quantity {2}".format(i_sell_check, DIC_candi_top_semi_company[i_sell_check], sellable_quantity_current))
                            cancel_order = cancel_toss_stock_order(token_get, DIC_transaction_top_semi_comp_SELL_target_with_orderID[i_sell_check])
                            DIC_transaction_top_semi_comp_SELL_target_with_orderID.pop(i_sell_check, None)   # 취소한 orderID는 삭제
                        time.sleep(0.1)

                    time.sleep(0.1)

                    '''
                    occupied_quantity = 0
                    for i_bought_check in DIC_candi_top_semi_company.keys() :
                        bought_check = get_sellable_quantity(token_get, i_bought_check)
                        print ("occupied quantity of {0}_{1} is {2:,}".format(i_bought_check, DIC_candi_top_semi_company[i_bought_check], int(bought_check)))
                        occupied_quantity = occupied_quantity + int(bought_check)
                    '''
                    

                    

                # [at 08:14]   general company 종목의, 매수한 종목별 average price를 추출하여 dictionary로 구성
                #elif ((market_condition != 0) and (8 <= now_in_mode.hour < 9) and (14 <= now_in_mode.minute < 15)) :
                elif (8 <= now_in_mode.hour < 9) and (14 <= now_in_mode.minute < 15) and (30 <= now_in_mode.second < 45) :
                    print ("making average bought price of each general company at ",  (datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600))))
                    
                    asset_current = asset_check (token_get)
                    print ("current asset : \n ", asset_current)

                    for i_average_price_15_t in DIC_candi_top_semi_company.keys() :
                        items_15_t = asset_current.get("result", {}).get("items", [])
                        target_item_15_t = next((item for item in items_15_t if str(item.get("symbol")) == i_average_price_15_t), None)

                        bought_quantity_top_semi_comp = get_sellable_quantity(token_get, i_average_price_15_t)
                        
                        print ("{0}_{1}_average bought price check".format(i_average_price_15_t, DIC_candi_top_semi_company[i_average_price_15_t]))

                        if target_item_15_t:
                            aver_price_15_t = target_item_15_t.get("averagePurchasePrice")
                            print("평균 매수가_{0}_{1} : {2:,} AND 매수 물량 {3:,}".format(i_average_price_15_t, DIC_candi_top_semi_company[i_average_price_15_t], aver_price_15_t, int(bought_quantity_top_semi_comp)))
                            DIC_top_semi_comp_bought_average_price[i_average_price_15_t] = aver_price_15_t
                            DIC_top_semi_comp_bought_quantity[i_average_price_15_t] = int(bought_quantity_top_semi_comp)

                        else:
                            print("해당 symbol을 찾을 수 없습니다.")
                        time.sleep(0.3)
                    print ("\nDIC_top_semi_comp_bought_average_price : \n", DIC_top_semi_comp_bought_average_price)
                    print ("\nDIC_top_semi_comp_bought_quantity : \n", DIC_top_semi_comp_bought_quantity)
                        

                    for i_average_price_15_g in DIC_candi_general_company.keys() :
                        items_15_g = asset_current.get("result", {}).get("items", [])
                        target_item_15_g = next((item for item in items_15_g if str(item.get("symbol")) == i_average_price_15_g), None)

                        bought_quantity_general_comp = get_sellable_quantity(token_get, i_average_price_15_g)
                        
                        print ("{0}_{1}_average bought price check".format(i_average_price_15_g, DIC_candi_general_company[i_average_price_15_g]))

                        if target_item_15_g:
                            aver_price_15_g = target_item_15_g.get("averagePurchasePrice")
                            print("평균 매수가_{0}_{1} : {2:,} AND 매수 물량 {3:,}".format(i_average_price_15_g, DIC_candi_general_company[i_average_price_15_g], aver_price_15_g, int(bought_quantity_general_comp)))
                            DIC_general_comp_bought_average_price[i_average_price_15_g] = aver_price_15_g
                            DIC_general_comp_bought_quantity[i_average_price_15_g] = int(bought_quantity_general_comp)

                        else:
                            print("해당 symbol을 찾을 수 없습니다.")
                        time.sleep(0.3)
                    print ("\nDIC_general_comp_bought_average_price : \n", DIC_general_comp_bought_average_price)
                    print ("\nDIC_general_comp_bought_quantity : \n", DIC_general_comp_bought_quantity)


                    total_bought_quantity = sum(DIC_top_semi_comp_bought_quantity.values()) + sum(DIC_general_comp_bought_quantity.values())

                    time.sleep(10)

                # [from 08:15]   08:01 또는 08:02에 매수한 general company 종목 매도    #elif (market_condition != 0) and (8 <= now_in_mode.hour < 9) and (15 <= now_in_mode.minute < 50) :
                elif (total_bought_quantity >= 1) and (8 <= now_in_mode.hour < 9) and (15 <= now_in_mode.minute < 50) :
                    print ("   \n\n\nSell transaction conducting at : ",  (datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600))))

                    for i_sell_general in DIC_general_comp_bought_average_price.keys() :
                        try_to_sell_quantity_15_g = get_sellable_quantity(token_get, i_sell_general)
                        print ("{0}_{1} is under checking of selling of GENERAL compamies with quantity : {2}".format(i_sell_general, DIC_candi_general_company[i_sell_general], try_to_sell_quantity_15_g))
                        if (try_to_sell_quantity_15_g >= 1) :
                            try_to_sell_quantity_15_g = get_sellable_quantity(token_get, i_sell_general)
                            bought_price_15_g = DIC_general_comp_bought_average_price[i_sell_general]
                            yesterday_finished_price_15_g = DIC_candi_general_company_yesterday_end_price[i_sell_general]
                            print ("average bought price is {0:,} and sellable quantity is {1:,}".format(bought_price_15_g, try_to_sell_quantity_15_g))
    
                            get_callable_ask_bid_price_info_sell_g = get_orderbook(token_get, str(i_sell_general)) # 해당 주식의 매도/매수 호가 및 연관 물량 조회
    
                            # 1. result 내부의 bids 배열 접근
                            bids = get_callable_ask_bid_price_info_sell_g.get("bids", [])
                            print( " bids price information : ", bids)
    
                            # 2. bids 배열에서 가장 높은 price 추출
                            callable_bid_price_0_15_g = max(int(bid["price"]) for bid in bids)
                            #callable_bid_price_0_15_g = int(get_callable_ask_bid_price_info_sell_g["bids"][0]["price"])   # 현재 첫번째로 높은 매수 호가 (현재 해당 주식을 어떤 사람이 사겠다고 제안한 가격)
    
                            if (callable_bid_price_0_15_g is not None) and (callable_bid_price_0_15_g >= (0.8 * yesterday_finished_price_15_g)) and ((callable_bid_price_0_15_g > bought_price_15_g) or (callable_bid_price_0_15_g <= (0.99 * bought_price_15_g))) :
                                order_response_sell_s, orderID_sell_s = run_toss_stock_buyer_seller(token_get, str(i_sell_general), "SELL", "LIMIT", try_to_sell_quantity_15_g, callable_bid_price_0_15_g)
                                time.sleep(0.5)
                                sellable_quantity_after_order_15_g = get_sellable_quantity(token_get, str(i_sell_general))
                                print ("\n{0}_{1} bought quantity after sell order is {2}".format(i_sell_general, DIC_candi_general_company[i_sell_general], sellable_quantity_after_order_15_g))
                                
                                if (order_response_sell_s == 1) :
                                    DIC_transaction_general_comp_SELL_target_with_orderID[i_sell_general] = orderID_sell_s
                                    print ("orderID_sell_s : ", orderID_sell_s)
                            time.sleep(0.1)
                            print ("DIC_transaction_general_comp_SELL_target_with_orderID :\n", DIC_transaction_general_comp_SELL_target_with_orderID)
                        time.sleep(0.1)
                        

                    # 매도 안된 주문은 취소하기
                    for i_sell_general_check in list(DIC_transaction_general_comp_SELL_target_with_orderID.keys()) :
                        sellable_quantity_current_15_g = get_sellable_quantity(token_get, str(i_sell_general_check))

                        if (sellable_quantity_current_15_g >= 1) :
                            print("UnSold quantity order is cenceled of {0}_{1} with quantity {2}".format(i_sell_general_check, DIC_candi_general_company[i_sell_general_check], sellable_quantity_current_15_g))
                            cancel_order = cancel_toss_stock_order(token_get, DIC_transaction_general_comp_SELL_target_with_orderID[i_sell_general_check])
                            DIC_transaction_general_comp_SELL_target_with_orderID.pop(i_sell_general_check, None)   # 취소한 orderID는 삭제
                        time.sleep(0.1)

                    print ("\n\n\nCurrent Time : ", (datetime.datetime.now() + datetime.timedelta(seconds=(time_conpensation_factor * 3600))))  # 클라우드 서버와 한국과의 시간차이 보정 (9시간)

                    time.sleep(0.1)


                    # 08:05~08:14:30 사이에 매도 안된 top_semi 매도

                    for i_sell in DIC_top_semi_comp_bought_average_price.keys() :
                        try_to_sell_quantity = get_sellable_quantity(token_get, i_sell)
                        print ("{0}_{1} is under checking of selling of TOP SEMI companies with quantity : {2:,}".format(i_sell, DIC_candi_top_semi_company[i_sell], try_to_sell_quantity))

                        if (try_to_sell_quantity >= 1) :
                            print ("{0}_{1} is under checking of selling of TOP SEMI companies".format(i_sell, DIC_candi_top_semi_company[i_sell]))
                            bought_price = DIC_top_semi_comp_bought_average_price[i_sell]
                            yesterday_finished_price = DIC_candi_top_semi_company_yesterday_end_price[i_sell]
                            print ("average bought price is {0:,} and sellable quantity is {1:,}".format(bought_price, try_to_sell_quantity))
    
                            get_callable_ask_bid_price_info_sell = get_orderbook(token_get, str(i_sell)) # 해당 주식의 매도/매수 호가 및 연관 물량 조회
    
                            # 1. result 내부의 bids 배열 안전하게 접근
                            bids_list = get_callable_ask_bid_price_info_sell.get("bids", [])
                            print("bids price information : ", bids_list)
    
                            # 2. 데이터 유무 확인 후 min()으로 최저가 추출
                            if bids_list :
                                callable_bid_price_0 = max(int(bid["price"]) for bid in bids_list)
                            
                            else :
                                callable_bid_price_0 = None
                                print("매수 호가 데이터가 존재하지 않습니다.")                       
                            #callable_bid_price_0 = int(get_callable_ask_bid_price_info_sell["bids"][0]["price"])   # 현재 첫번째로 높은 매수 호가 (현재 해당 주식을 어떤 사람이 사겠다고 제안한 가격)
    
                            if (callable_bid_price_0 is not None) and (try_to_sell_quantity >= 1) and (callable_bid_price_0 >= (0.8 * yesterday_finished_price)) and ((callable_bid_price_0 > bought_price) or (callable_bid_price_0 <= (0.99 * bought_price))) :
                                order_response_sell, orderID_sell = run_toss_stock_buyer_seller(token_get, str(i_sell), "SELL", "LIMIT", try_to_sell_quantity, callable_bid_price_0)
                                time.sleep(0.5)
                                sellable_quantity_after_order = get_sellable_quantity(token_get, str(i_sell))
                                print ("\n{0}_{1} bought quantity after sell order is {2}".format(i_sell, DIC_candi_top_semi_company[i_sell], sellable_quantity_after_order))
                                
                                if (order_response_sell == 1) :
                                    DIC_transaction_top_semi_comp_SELL_target_with_orderID[i_sell] = orderID_sell
                                    print ("orderID_sell : ", orderID_sell)                                
                            time.sleep(0.1)
                            print("DIC_transaction_top_semi_comp_SELL_target_with_orderID :\n", DIC_transaction_top_semi_comp_SELL_target_with_orderID)
                        time.sleep(0.1)
                        

                    # 매도 안된 주문은 취소하기
                    for i_sell_check in list(DIC_transaction_top_semi_comp_SELL_target_with_orderID.keys()) :
                        sellable_quantity_current = get_sellable_quantity(token_get, str(i_sell_check))

                        if (sellable_quantity_current >= 1) :
                            print("UnSold quantity order is cenceled of {0}_{1} with quantity {2}".format(i_sell_check, DIC_candi_top_semi_company[i_sell_check], sellable_quantity_current))
                            cancel_order = cancel_toss_stock_order(token_get, DIC_transaction_top_semi_comp_SELL_target_with_orderID[i_sell_check])
                            DIC_transaction_top_semi_comp_SELL_target_with_orderID.pop(i_sell_check, None)   # 취소한 orderID는 삭제
                        time.sleep(0.1)

                

                
                
                elif ((8 <= now_in_mode.hour < 9) and (55 <= now_in_mode.minute < 56) and (0 <= now_in_mode.second < (cycle_in_transation_mode + 3))) :
                    total_cash_buyable_today = 0
                    money_for_a_item_divider_for_top_semi_comp = 2
                    money_for_a_item_divider_for_general_comp = 5
                    
                    money_for_buy_a_top_semi_comp = 0
                    total_cash_buyable_residual = 0
                    total_cash_buyable_residual_s = 0
                     
                    DIC_candi_top_semi_company_yesterday_end_price = {}
                    DIC_candi_general_company_yesterday_end_price = {}
                    
                    DIC_candi_top_semi_company_0800_start_price = {}
                    DIC_candi_general_company_0800_start_price = {}
                    
                    DIC_candi_top_semi_company_0801_start_price = {}
                    DIC_candi_general_company_0801_start_price = {}
                    
                    DIC_candi_top_semi_company_0802_start_price = {}
                    DIC_candi_general_company_0802_start_price = {}
                    
                    DIC_candi_company_ratio_top_semi_comp_0800_to_yesterday = {}
                    DIC_candi_company_ratio_general_comp_0800_to_yesterday = {}
                    
                    DIC_candi_company_ratio_top_semi_comp_0801_to_yesterday = {}
                    DIC_candi_company_ratio_general_comp_0801_to_yesterday = {}
                    
                    DIC_candi_company_ratio_top_semi_comp_0802_to_yesterday = {}
                    DIC_candi_company_ratio_general_comp_0802_to_yesterday = {}
                    
                    DIC_candi_company_ratio_top_semi_comp_0801_to_0800 = {}
                    DIC_candi_company_ratio_general_comp_0801_to_0800 = {}
                    
                    DIC_candi_company_ratio_top_semi_comp_0802_to_0801 = {}
                    DIC_candi_company_ratio_general_comp_0802_to_0801 = {}
                    
                    median_ratio_top_semi_comp_0800_yesterday = 0
                    median_ratio_general_comp_0800_yesterday = 0
                    
                    DIC_transaction_top_semi_comp_buy_target_quantity = {}
                    DIC_transaction_general_comp_buy_target_quantity = {}
                    
                    DIC_candi_top_semi_company_transaction_money_0800_0801 = {}
                    DIC_candi_general_company_transaction_money_0800_0801 = {}
                    
                    DIC_candi_top_semi_company_transaction_money_0800_0802 = {}
                    DIC_candi_general_company_transaction_money_0800_0802 = {}
                    
                    DIC_transaction_top_semi_comp_buy_target_with_orderID = {}
                    DIC_transaction_general_comp_buy_target_with_orderID = {}
                    
                    DIC_transaction_top_semi_comp_SELL_target_with_orderID = {}
                    DIC_transaction_general_comp_SELL_target_with_orderID = {}
                    
                    DIC_top_semi_comp_bought_average_price = {}
                    DIC_general_comp_bought_average_price = {}
                    
                    DIC_top_semi_comp_bought_quantity = {}
                    DIC_general_comp_bought_quantity = {}
                    
                    total_bought_quantity = 0
                    
                    market_condition = 99
                    
                    #buy_state = 0
                    
                    #bought_quantity_of_0 = 0
                    #bought_quantity_of_1 = 0
                    
                    intermediate_price = 0
                    
                    order_response = 0


                time.sleep(cycle_in_transation_mode)
                #time_check = time_check + 1

        time.sleep(cycle_period)

    except :
        
        print ('\n\nError has occured!!!')
        err_msg = traceback.format_exc()
        print(err_msg)
        time.sleep(10)


# In[ ]:


#test_asset_check = asset_check(token_get)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




