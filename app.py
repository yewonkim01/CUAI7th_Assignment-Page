import streamlit as st
import pandas as pd
import numpy as np

import qa_settings
from DB_class import DB
from submit_df import submit_df
from email_info import email_set, data


#이메일로 로그인
def login_email() -> tuple:
    email = st.text_input("본인의 이메일로 로그인하세요.")

    if email in email_set:
        name = data.get(email)
        st.markdown(f' :green[[CUAI 7기 BASIC Track]] {name} {email}')
        return True, name, email
    else:
        st.markdown(' :green[CUAI에 등록된 이메일을 입력해주세요.]')
        return (False,)

#정답출력 함수
def show_ans(A:str):    
    ans_css = """
        <style>
            .ans-rounded-box {
                border-radius: 10px;
                background-color: #45435A;
                padding: 20px;
                height: 200px;
                margin-right:10px;
                margin-bottom:20px;
            }
        </style>
    """
    # CSS 적용 마크다운
    st.markdown(ans_css, unsafe_allow_html=True)  

    # 둥근 사각형 안에 글씨 출력
    st.markdown('정답 확인')
    st.markdown(f'<div class="ans-rounded-box">{A}</div>', unsafe_allow_html=True)


def all(qs:list, As:list, chapter:str, chapter_name:str, name:str, email:str):
    #qs: 해당 주차 문제 담긴 리스트
    #As: 해당 주차 정답 담긴 리스트
    #chapter: 챕터    ex)ch01 (db에 저장되는 collection 이름)
    #chapter_name: 챕터이름 ex)차원축소
    #name: 학회원 이름
    #email: 학회원 이메일

    # 페이지 서브헤더 제목 설정
    st.subheader(f"[Chapter{chapter[2:]}] {chapter_name}")

    #문제들을 tab으로 구현
    tab1, tab2, tab3, tab4, tab5 = st.tabs([f'Q{i}' for i in range(1, len(qs)+1)])
    tabs = [tab1, tab2, tab3, tab4, tab5]

    db = DB(chapter, name)
    
    #존재하는 tab수만큼 반복문 돌리면서 화면 구성
    for i in range(len(tabs)):

        with tabs[i]:
            col1, col2 = st.columns(2)  #col1은 왼쪽 문제보이는 열, col2는 오른쪽 답변과 정답확인하는 열 

            #왼쪽 문제 열
            with col1:
                st.write("")
                css = """
                    <style>
                        .rounded-box {
                            border-radius: 10px;
                            background-color: #45435A;
                            padding: 20px;
                            height: 600px;
                            margin-right:10px;
                        }
                    </style>
                """
                # CSS 적용
                st.markdown(css, unsafe_allow_html=True)
                #qs는 문제가 담긴 리스트  
                q = qs[i]

                # 둥근 사각형 만들어서 안에 문제 적기
                st.markdown(f'<div class="rounded-box">{q}</div>', unsafe_allow_html=True)


            #오른쪽 답변/정답 열
            with col2:
                st.write('\n')

                #이미 제출한 답변이 있으면 기본값(value)으로 답변작성란에 띄워지도록
                submitted_ans = db.submitted_answer(i)
                
                #제출한 답변 있으면
                if submitted_ans:
                    value = submitted_ans
                #제출한 답변 없으면 ""(빈칸)
                else:
                    value = ""
                answer = st.text_area("", key = f"ans{i+1}", height=200, placeholder="답안을 작성해 주세요.", value = value)

                #제출하기 button
                button = st.button("제출하기", key=f"button{i+1}")

                #제출된 답변 있으면 정답화면 바로 보이게/
                submits = db.submitted_check(qs) #submits = [1,0,1,1,1]
                if submits[i]:
                    st.markdown(' :green[☑ 제출되었습니다.]')
                    show_ans(As[i])

                #제출된 답변 없으면 <제출하기> 버튼 눌러야 정답확인 가능 
                if len(answer.strip()) >= 10:   #10글자 이상 작성

                    if button:
                        #이미 제출했는데 버튼 또 누르면(재제출)
                        if submits[i]:
                            #st.balloons() 풍선나옴!!
                            #db에만 답변 저장
                            db.save_db(i+1, answer)
                            
                        #처음 제출이면
                        else:
                            db.save_db(i+1, answer)
                            #제출문구 띄우고 답변 보여주기
                            st.markdown(' :green[☑ 제출되었습니다.]')
                            show_ans(As[i])
                        q,w,e,r,t = st.columns(5)
                        with t:
                            st.button("다음 문제로 이동>") #이거 작동안함 / tab으로 구현했는데 어떻게 연결할지 모르겠음
                        
                else:
                    st.markdown('10자 이상 작성해주세요.')
                

            
if __name__ == "__main__":
    qs = qa_settings.qs
    As = qa_settings.As
    chapter = qa_settings.chapter
    chapter_name = qa_settings.chapter_name

    #페이지 기본 설정
    st.set_page_config(
        #page_icon=""
        page_title="CUAI 7기 BASIC Track assignment",
        layout = "wide",
    )

    col1, col2 = st.columns(2)
    with col1:
        #이메일로 로그인
        login_result = login_email() #tuple로 반환 (db에 등록된 이메일인지 여부, 이름, 이메일)


    
    if login_result[0]:
        name, email = login_result[1:]
        all(qs, As, chapter, chapter_name, name, email)

        #상단 오른쪽에 제출했는지 데이터프레임 보여주기
        with col2:
            a,b = st.columns(2)
            with b:
                submit_df(chapter, name, len(qs))


                
    




