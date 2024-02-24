import streamlit as st
import pandas as pd

from DB_class import DB

"""
오른쪽 상단 제출여부 알려주는 데이터프레임 반환해주는 함수
"""

def submit_df(chapter, name, num_q):
    db = DB(chapter, name)
    doc_field = db.doc_field

    #제출했으면 O표시 초록색으로
    def select_color(value):
        if value == 'O':
            return 'color:green'
        else:
            return 'color:red'

    #제출되었는지 여부/ 제출완료는 O, 미제출은 ""
    def check_db_submitted(value):
        if value in doc_field.keys():
            return 'O'
        else:
            return ''
    
    #데이터프레임 생성
    df = pd.DataFrame(
        {f'Q{i}':check_db_submitted(f"Q{i}") for i in range(1, num_q+1)}
        , index = ['제출'])
    
    #값에 select_color() 적용
    style_df = df.style.applymap(lambda x: select_color(x))
    st.dataframe(style_df, width=305)
    
    if df.eq('O').all().all():
        st.markdown(f' :green[모든 문제를 제출했습니다.]')