import streamlit as st
import pandas as pd

from DB_class import DB
import pytz
from datetime import datetime


"""
오른쪽 상단 제출여부 알려주는 데이터프레임 반환해주는 함수
"""

def submit_df(chapter, name, num_q):
    kst = pytz.timezone('Asia/Seoul')
    now = datetime.now(kst)
    
    #date도 저장
    date = now.strftime("%Y.%m.%d %H:%M")
    db = DB(chapter, name)
    doc_field_keys = db.doc_field.keys()

    #제출했으면 O표시 초록색으로
    def select_color(value):
        if value == 'O':
            return 'color:green'
        else:
            return 'color:red'

    #제출되었는지 여부/ 제출완료는 O, 미제출은 ""
    def check_db_submitted(value):
        if value in doc_field_keys:
            return 'O'
        else:
            return ''

    
    #데이터프레임 생성
    df = pd.DataFrame(
        {f'Q{i}':check_db_submitted(f"Q{i}") for i in range(1, num_q+1)}
        , index = ['제출'])
    
    #값에 select_color() 적용
    style_df = df.style.applymap(lambda x: select_color(x))
    
    if df.eq('O').all().all():
        st.dataframe(style_df, width=305)
        st.markdown(f'✅:green[{date} 모든 문제 제출 완료]')
        db.doc_ref.update({
            "FINAL_SUBMIT":
            date[2:]})
    else:
        st.dataframe(style_df, width=305)
        st.markdown(f'❌:red[미제출된 항목이 있습니다.]')
