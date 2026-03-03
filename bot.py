import os
import requests

# 깃허브 금고 열쇠
ALIGO_KEY = os.environ.get('ALIGO_API_KEY')
ALIGO_SENDER = os.environ.get('ALIGO_SENDER_KEY')
ALIGO_USER = os.environ.get('ALIGO_USER_ID')

# ⚠️ 템플릿 문구 (알리고 관리자 화면과 100% 일치해야 함)
ALIGO_TEMPLATE_CODE = "UF_7303"
MESSAGE_BODY = """#{고객명}님, #{상품명}을 주문해 주셔서 감사합니다. 아래 링크에서 가계부를 다운로드 해주세요. #{고객님}의 자산이 차곡차곡 쌓이길 응원하겠습니다❤️"""

def send_kakao_notification(phone, customer_name):
    # 가장 표준적인 주소
    url = "https://apis.aligo.in/akv10/alimtalk/send/"
    
    # 변수 치환
    final_message = MESSAGE_BODY.replace("#{고객명}", customer_name) \
                               .replace("#{상품명}", "가계부") \
                               .replace("#{고객님}", customer_name)

    # 요청 데이터
    payload = {
        "key": ALIGO_KEY,
        "userid": ALIGO_USER,
        "senderkey": ALIGO_SENDER,
        "tpl_code": ALIGO_TEMPLATE_CODE,
        "receiver_1": phone,
        "subject_1": "가계부 배송 안내",
        "message_1": final_message,
    }

    # 💡 헤더 추가 (브라우저인 척 하기)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        print(f"📡 알리고 서버에 접속 시도 중... (수신인: {customer_name})")
        response = requests.post(url, data=payload, headers=headers, timeout=15)
        
        print(f"📩 서버 응답 상태 코드: {response.status_code}")
        
        # JSON 분석 시도
        try:
            result = response.json()
            if result.get('result_code') == '1':
                print(f"✅ 발송 성공!")
            else:
                print(f"❌ 알리고 거절 사유: {result.get('message')}")
        except:
            print("🚨 서버가 JSON이 아닌 HTML 에러 페이지를 보냈습니다.")
            print(f"상세 내용(앞부분): {response.text[:300]}")

    except Exception as e:
        print(f"🚨 연결 실패! 원인: {e}")

if __name__ == "__main__":
    print("[재테콩 시스템] 테스트를 시작합니다.")
    send_kakao_notification("01097675153", "대원")
