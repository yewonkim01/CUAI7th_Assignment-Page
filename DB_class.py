from google.cloud import firestore

import pytz
from datetime import datetime
import streamlit as st
import pandas as pd



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
            self.doc_field_keys = self.doc_field.keys()

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
        #st.rerun()

    
    
    #제출한 문제인지 db에서 확인
    def submitted_check(self, qs:list) -> list: #반환값은 문제 순서에 맞게 [1,0,1,1,1] (2번 문제를 제출 안한 것)
        q_list = [i for i in list(self.doc_field_keys) if i[0] == 'Q']
        q_list = [int(i[1]) for i in q_list]
        submitted_list = [1 if i in q_list else 0 for i in range(1, len(qs)+1)]
        return submitted_list
    

    #이미 이전에 작성한 내용있으면 DB에서 가져오기 없으면 "" 반환
    def submitted_answer(self, q_num:int) -> str: #반환값은 이미 작성했던 답변
        if f"Q{q_num}" in self.doc_field_keys:
            return self.doc_field[f"Q{q_num}"]['ans']
        else:
            return ""
        
    #제출했으면 O표시 초록색으로
    def select_color(self, value):
        if value == 'O':
            return 'color:green'
        else:
            return 'color:red'
    
    #제출되었는지 여부/ 제출완료는 O, 미제출은 ""
    def check_db_submitted(self, value):
        if value in self.doc_field_keys:
            return 'O'
        else:
            return ''
        
    def submit_df(self):
        print('submit_df ing')
        kst = pytz.timezone('Asia/Seoul')
        now = datetime.now(kst)
        
        #date도 저장
        date = now.strftime("%Y.%m.%d %H:%M")
        
        #데이터프레임 생성
        df = pd.DataFrame(st.session_state.value, index = ['제출'])
        
        #값에 select_color() 적용
        style_df = df.style.applymap(lambda x: self.select_color(x))
        st.dataframe(style_df, width=440)

        if not st.session_state.button_pressed and st.session_state['FINAL_SUBMIT']:
            f = st.session_state['FINAL_SUBMIT'][2:]
            st.markdown(f'✅:green[{f} 모든 문제 제출 완료]')
        else:
            if df.eq('O').all().all():
                st.session_state.submitted = True
                st.session_state['FINAL_SUBMIT'] = date[2:]
                st.markdown(f'✅:green[{date[2:]} 모든 문제 제출 완료]')
                self.doc_ref.update({
                    "FINAL_SUBMIT":
                    date[2:]})
                st.session_state.button_pressed = False
                    
            else:
                st.markdown(f' :red[미제출된 항목이 있습니다.]')
                st.session_state.button_pressed = False

    def check_FINAL_SUBMIT(self):
        if 'FINAL_SUBMIT' in self.doc_field:
            return self.doc_field['FINAL_SUBMIT']
        else:
            return ""
