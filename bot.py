import os
import requests
import json

# 1. 깃허브 Secrets에서 안전하게 정보를 가져옵니다.
ALIGO_KEY = os.environ.get('ALIGO_API_KEY')
ALIGO_SENDER = os.environ.get('ALIGO_SENDER_KEY')
ALIGO_USER = os.environ.get('ALIGO_USER_ID')

# --- ⚠️ 알리고 템플릿 정보 ⚠️ ---
ALIGO_TEMPLATE_CODE = "UF_7303" 
MESSAGE_BODY = """#{고객명}님, #{상품명}을 주문해 주셔서 감사합니다. 아래 링크에서 가계부를 다운로드 해주세요. #{고객님}의 자산이 차곡차곡 쌓이길 응원하겠습니다❤️"""
# ------------------------------

def send_kakao_notification(phone, customer_name):
    """알리고를 통한 알림톡 실제 발송 (표준 주소 사용)"""
    
    # 💡 DNS 에러 해결을 위해 가장 표준적인 apis.aligo.in 주소를 사용합니다.
    url = "https://apis.aligo.in/akv10/alimtalk/send/"
    
    final_message = MESSAGE_BODY.replace("#{고객명}", customer_name) \
                               .replace("#{상품명}", "가계부") \
                               .replace("#{고객님}", customer_name)

    # 알리고 API 요구사항에 맞춰 데이터를 준비합니다.
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
        # 💡 타임아웃(timeout)을 추가하여 무한 대기를 방지합니다.
        response = requests.post(url, data=payload, timeout=10)
        
        # 응답이 왔는지 확인
        if response.status_code == 200:
            try:
                result = response.json()
                if result.get('result_code') == '1':
                    print(f"✅ 알림톡 발송 성공: {customer_name}님")
                else:
                    print(f"❌ 알리고 거절: {result.get('message')}")
            except:
                print(f"🚨 알리고가 이상한 응답을 보냈습니다 (HTML 에러 페이지일 가능성).")
                print(f"내용 확인: {response.text[:100]}")
        else:
            print(f"🚨 서버 연결 실패 (상태 코드: {response.status_code})")
            
    except Exception as e:
        print(f"🚨 연결 과정에서 오류 발생: {e}")

if __name__ == "__main__":
    print(f"[재테콩] 가계부 자동 발송 시스템 가동...")
    # 테스트 발송
    send_kakao_notification("01097675153", "대원") 
    print("작업이 완료되었습니다.")
