from google.cloud import firestore
from datetime import datetime
import pytz

"""
firestore DB 연결해주는 클래스
"""

class DB:
    def __init__(self, chapter, name):
        #콜렉션은 챕터 이름
        self.collection = firestore.Client.from_service_account_json("key.json")\
            .collection(chapter)
        if name:
            self.doc_ref = self.collection.document(name)
            self.doc_field = self.doc_ref.get()._data

    #firestore_registerName.py에서 쓰임(DB에 챕터명, 학회원들 이름 등록하는 함수)
    def register_name(self, name):
        self.doc_ref = self.collection.document(name)
        self.doc_ref.set(0)

    #db에 저장
    def save_db(self, num:int, answer:str):
        kst = pytz.timezone('Asia/Seoul')
        now = datetime.now(kst)
        
        #date도 저장
        date = now.strftime("%Y/%m/%d %H:%M")
        self.doc_ref.update({
            f"Q{num}":{f'ans':answer, "date":date}
        })
        return 
    
    #제출한 문제인지 db에서 확인
    def submitted_check(self, qs:list) -> list: #반환값은 문제 순서에 맞게 [1,0,1,1,1] (2번 문제를 제출 안한 것)
        q_list = list(self.doc_field.keys())
        q_list = [int(i[1]) for i in q_list]
        submitted_list = [1 if i in q_list else 0 for i in range(1, len(qs)+1)]
        return submitted_list
    

    #이미 이전에 작성한 내용있으면 DB에서 가져오기 없으면 "" 반환
    def submitted_answer(self, q_num:int) -> str: #반환값은 이미 작성했던 답변
        if f"Q{q_num+1}" in self.doc_field.keys():
            return self.doc_field[f"Q{q_num+1}"]['ans']
        else:
            return ""