import os
import requests
import json

# 1. 깃허브 Secrets에서 정보 가져오기
ALIGO_KEY = os.environ.get('ALIGO_API_KEY')
ALIGO_SENDER = os.environ.get('ALIGO_SENDER_KEY')
ALIGO_USER = os.environ.get('ALIGO_USER_ID')

ALIGO_TEMPLATE_CODE = "UF_7303" 
MESSAGE_BODY = """#{고객명}님, #{상품명}을 주문해 주셔서 감사합니다. 아래 링크에서 가계부를 다운로드 해주세요. #{고객님}의 자산이 차곡차곡 쌓이길 응원하겠습니다❤️"""

def send_kakao_notification(phone, customer_name):
    # 원래의 안정적인 주소로 다시 시도해봅니다.
    url = "https://alimtalk-api.aligo.in/akv10/alimtalk/send/"
    
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
        
        # 💡 만약 응답이 JSON이 아니면 어떤 내용인지 직접 출력합니다.
        try:
            result = response.json()
            if result.get('result_code') == '1':
                print(f"✅ 알림톡 발송 성공: {customer_name}님")
            else:
                print(f"❌ 발송 실패: {result.get('message')}")
        except:
            print("🚨 알리고 서버에서 예상치 못한 응답을 보냈습니다.")
            print(f"상태 코드: {response.status_code}")
            print(f"응답 내용: {response.text[:200]}") # 에러 페이지 내용 일부 출력
            
    except Exception as e:
        print(f"🚨 네트워크 오류 발생: {e}")

if __name__ == "__main__":
    print("[20260224-001] 주문 처리 시작...")
    # 테스트 번호로 실행
    send_kakao_notification("01097675153", "대원")
    print("[20260224-001] 작업 완료")
