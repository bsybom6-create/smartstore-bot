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

# --- ⚠️ 여기만 정확하게 확인해 주세요 ⚠️ ---
ALIGO_TEMPLATE_CODE = "UF_7303" 
# 승인받은 문구와 토씨 하나 틀리지 않게 입력해야 합니다.
MESSAGE_BODY = """#{고객명}님, #{상품명}을 주문해 주셔서 감사합니다. 아래 링크에서 가계부를 다운로드 해주세요. #{고객님}의 자산이 차곡차곡 쌓이길 응원하겠습니다❤️"""
# ----------------------------------------------

def get_naver_token():
    """네이버 API 접속 (현재는 뼈대 코드)"""
    return "NAVER_ACCESS_TOKEN"

def process_smartstore_orders(token):
    """테스트용 주문 데이터 처리"""
    new_orders = [
        {"id": "20260224-001", "name": "대원", "phone": "01097675153"} # 대원님 번호로 테스트
    ]

    for order in new_orders:
        print(f"[{order['id']}] 주문 처리 시작...")
        send_kakao_notification(order['phone'], order['name'])
        print(f"[{order['id']}] 작업 완료")

def send_kakao_notification(phone, customer_name):
    """알리고를 통한 알림톡 실제 발송"""
    # 💡 연결 오류 해결을 위해 더 안정적인 API 주소(apis.aligo.in)로 변경했습니다.
    url = "https://apis.aligo.in/akv10/alimtalk/send/"
    
    # 💡 중요: 템플릿에 있는 '모든' 변수를 실제 값으로 바꿔줘야 발송에 실패하지 않습니다.
    final_message = MESSAGE_BODY.replace("#{고객명}", customer_name) \
                               .replace("#{상품명}", "가계부") \
                               .replace("#{고객님}", customer_name)

    payload = {
        "key": ALIGO_KEY,
        "userid": ALIGO_USER,
        "senderkey": ALIGO_SENDER,
        "tpl_code": ALIGO_TEMPLATE_CODE,
        "receiver_1": phone,
        "subject_1": "가계부 배송 안내",
        "message_1": final_message,
    }
    
    try:
        response = requests.post(url, data=payload)
        result = response.json()
        if result.get('result_code') == '1':
            print(f"✅ 알림톡 발송 성공: {customer_name}님")
        else:
            print(f"❌ 발송 실패: {result.get('message')}")
    except Exception as e:
        print(f"🚨 네트워크 오류 발생: {e}")

if __name__ == "__main__":
    try:
        process_smartstore_orders(get_naver_token())
    except Exception as e:
        print(f"오류 발생: {e}")
