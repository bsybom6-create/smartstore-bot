import os
import requests
import json

# 1. 깃허브 Secrets에서 정보 가져오기
API_KEY = os.environ.get('ALIGO_API_KEY')
USER_ID = os.environ.get('ALIGO_USER_ID')
SENDER_KEY = os.environ.get('ALIGO_SENDER_KEY')

# --- ⚠️ 템플릿 및 발신자 정보 (이미지 358838 기반) ---
ALIGO_TEMPLATE_CODE = "UF_7303" 
SENDER_PHONE = "01097675153" # 알리고에 등록된 발신번호
MESSAGE_BODY = """#{고객명}님, #{상품명}을 주문해 주셔서 감사합니다. 아래 링크에서 가계부를 다운로드 해주세요. #{고객님}의 자산이 차곡차곡 쌓이길 응원하겠습니다❤️"""

# 만약 템플릿에 '웹링크' 버튼이 하나 있다면 아래 주석을 해제하고 정보를 입력하세요.
# BUTTON_INFO = json.dumps({
#     "button": [{"name": "가계부 다운로드", "linkType": "WL", "linkTypeName": "웹링크", "linkM": "모바일링크", "linkP": "PC링크"}]
# })
BUTTON_INFO = None 
# ----------------------------------------------

def get_aligo_token():
    """1단계: 토큰 생성"""
    url = "https://kakaoapi.aligo.in/akv10/token/create/30/s/"
    payload = {'apikey': API_KEY, 'userid': USER_ID}
    try:
        response = requests.post(url, data=payload, timeout=15)
        res_data = response.json()
        if res_data.get('code') == 0:
            return res_data.get('token')
        print(f"❌ 토큰 생성 실패: {res_data.get('message')}")
    except Exception as e:
        print(f"🚨 토큰 서버 접속 에러: {e}")
    return None

def send_alimtalk(token, phone, customer_name):
    """2단계: 알림톡 발송"""
    url = "https://kakaoapi.aligo.in/akv10/alimtalk/send/"
    
    final_message = MESSAGE_BODY.replace("#{고객명}", customer_name) \
                               .replace("#{상품명}", "가계부") \
                               .replace("#{고객님}", customer_name)

    payload = {
        'apikey': API_KEY,
        'userid': USER_ID,
        'token': token,
        'senderkey': SENDER_KEY,
        'tpl_code': ALIGO_TEMPLATE_CODE,
        'sender': SENDER_PHONE,
        'receiver_1': phone,
        'recvname_1': customer_name,
        'subject_1': '가계부 발송 안내',
        'message_1': final_message
    }
    
    if BUTTON_INFO:
        payload['button_1'] = BUTTON_INFO # 버튼 정보 추가

    try:
        response = requests.post(url, data=payload, timeout=20)
        res_data = response.json()
        if res_data.get('code') == 0:
            print(f"✅ 발송 성공: {customer_name}님")
        else:
            print(f"❌ 발송 실패: {res_data.get('message')}")
    except Exception as e:
        print(f"🚨 발송 서버 접속 에러: {e}")

if __name__ == "__main__":
    print("[재테콩] 정식 가이드 기반 시스템 가동")
    token = get_aligo_token()
    if token:
        # 테스트 발송
        send_alimtalk(token, "01097675153", "대원")
