import os
import requests
import time
import json

# 1. 깃허브 Secrets에서 안전하게 정보를 가져옵니다.
NAVER_ID = os.environ.get('NAVER_CLIENT_ID')
NAVER_SECRET = os.environ.get('NAVER_CLIENT_SECRET')
ALIGO_KEY = os.environ.get('ALIGO_API_KEY')
ALIGO_SENDER = os.environ.get('ALIGO_SENDER_KEY')
ALIGO_USER = os.environ.get('ALIGO_USER_ID')

# --- ⚠️ 여기 두 줄만 본인의 정보로 수정하세요 ⚠️ ---
ALIGO_TEMPLATE_CODE = "UF_6744"  # 알리고 '템플릿 관리'에 있는 코드 (예: TM_1234)
MESSAGE_BODY = """#{고객명}님. #{상품명}을 주문해 주셔서 감사합니다. 아래 링크를 통해 가계부를 다운받으실 수 있습니다. #{고객님}의 자산이 차곡차곡 쌓이길 응원하겠습니다❤️""" # 알리고에서 승인받은 '본문' 문구 그대로 입력
# ----------------------------------------------

def get_naver_token():
    """네이버 API 접속을 위한 통행증(Token) 발급"""
    url = "https://accounts.commerce.naver.com/api/v1/oauth2/token"
    # 실제 구현 시에는 ID/Secret을 조합한 인증 로직이 들어갑니다.
    # 지금은 흐름을 잡기 위한 구조입니다.
    return "NAVER_ACCESS_TOKEN"

def process_smartstore_orders(token):
    """신규 주문 확인 -> 발주 확인 -> 알림톡 발송 -> 배송 완료 처리"""
    
    # 실제로는 네이버 주문 조회 API를 호출합니다.
    # 예시: 새로운 주문이 1건 있다고 가정 (이름: 홍길동, 번호: 01012345678)
    new_orders = [
        {"id": "20260224-001", "name": "홍길동", "phone": "01012345678"}
    ]

    for order in new_orders:
        print(f"[{order['id']}] 주문 처리 시작...")
        
        # 1. 발주 확인 처리 (네이버 서버에 '확인했음' 알림)
        # 2. 알림톡 발송
        send_kakao_notification(order['phone'], order['name'])
        
        # 3. 배송 완료 처리 (디지털 상품이므로 즉시 발송 완료)
        print(f"[{order['id']}] 처리 완료 및 알림톡 발송 성공!")

def send_kakao_notification(phone, customer_name):
    """알리고를 통한 알림톡 실제 발송"""
    url = "https://alimtalk-api.aligo.in/akv10/alimtalk/send/"
    
    # 템플릿 문구 내 #{고객명} 부분을 실제 이름으로 교체합니다.
    final_message = MESSAGE_BODY.replace("#{고객명}", customer_name)

    payload = {
        "key": ALIGO_KEY,
        "userid": ALIGO_USER,
        "senderkey": ALIGO_SENDER,
        "tpl_code": ALIGO_TEMPLATE_CODE,
        "receiver_1": phone,
        "subject_1": "PDF 파일 발송",
        "message_1": final_message,
    }
    
    response = requests.post(url, data=payload)
    result = response.json()
    
    if result.get('result_code') == '1':
        print(f"알림톡 발송 완료: {customer_name}님")
    else:
        print(f"발송 실패 사유: {result.get('message')}")

if __name__ == "__main__":
    # 공장 가동!
    try:
        naver_token = get_naver_token()
        process_smartstore_orders(naver_token)
    except Exception as e:
        print(f"오류 발생: {e}")
