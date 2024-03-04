import streamlit as st

import qa_settings
from DB_class import DB
from submit_df import submit_df
from email_info import data
from datetime import datetime



#이메일로 로그인
def login_email() -> tuple:
    email = st.text_input("본인의 이메일로 로그인하세요.")
    email = email.strip()

    if email in data.keys():
        name = data.get(email)
        st.markdown(f' :green[[CUAI 7기 BASIC Track]] {name} {email}')
        return True, name, email
    else:
        st.markdown(' :green[CUAI에 등록된 이메일을 입력해주세요.]')
        return (False,)

#정답출력 함수
def show_answer(A:str):    
    ans_css = """
        <style>
            .ans-rounded-box {
                border-radius: 10px;
                background-color: #45435A;
                padding: 20px;
                height: 260px;
                margin-right:10px;
                margin-bottom:20px;
                overflow-y: auto;
            }
        </style>
    """
    # CSS 적용 마크다운
    st.markdown(ans_css, unsafe_allow_html=True)  

    # 둥근 사각형 안에 글씨 출력
    st.markdown('정답 확인')
    st.markdown(f'<div class="ans-rounded-box">{A}</div>', unsafe_allow_html=True)


def all(deadline:str, Qs:list, As:list, chapter:str, chapter_name:str, name:str, email:str):
    '''
    Qs: 해당 주차 문제 담긴 리스트
    As: 해당 주차 정답 담긴 리스트
    chapter: 챕터    ex)ch01 (db에 저장되는 collection 이름)
    chapter_name: 챕터이름 ex)차원축소
    name: 학회원 이름
    email: 학회원 이메일
    '''

    # 페이지 서브헤더 제목 설정
    st.subheader(f"[Chapter{chapter[2:]}] {chapter_name}")

    #문제들을 tab으로 구현
    tabs = st.tabs([f'Q{i}' for i in range(1, len(Qs)+1)])

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
                #Qs는 문제가 담긴 리스트  
                q = Qs[i]

                # 둥근 사각형 만들어서 안에 문제 적기
                st.markdown(f'<div class="rounded-box">{q}</div>', unsafe_allow_html=True)

            # 오른쪽 답변/정답 열
            with col2:
                st.write('\n')

                # 이미 제출한 답변이 있으면 기본값(value)으로 답변작성란에 띄워지도록
                submitted_ans = db.submitted_answer(i)
                
                answer = st.text_area(" ", key = f"ans{i+1}", height=200, placeholder="답안을 10자 이상 작성해 주세요.", value=submitted_ans)

                a,b,c,d = st.columns(4)
                with a:
                    # 제출하기 button
                    button = st.button("제출하기", key=f"button{i+1}", disabled= (len(answer.strip()) < 10))

                with d:
                    # # 제출된 답변 있으면 정답화면 바로 보이게/
                    submits = db.submitted_check(Qs) #submits = [1,0,1,1,1]
                    if submits[i]:
                        st.markdown(' :green[☑ 제출되었습니다.]')
                        
                if submits[i]: show_answer(As[i])

                # 제출된 답변 없으면 <제출하기> 버튼 눌러야 정답확인 가능 
                if button:
                    now = datetime.now()
                    if now > deadline:
                        st.error('과제제출 기한이 지나 제출할 수 없습니다.')
                    else:
                        # 이미 제출했는데 버튼 또 누르면(재제출)
                        if submits[i]:
                            # db에만 답변 저장
                            db.save_db(i+1, answer)
                            st.rerun()
                            
                        # # 처음 제출이면
                        else:
                            db.save_db(i+1, answer)
                            # 제출문구 띄우고 답변 보여주기
                            with d: st.markdown(' :green[☑ 제출되었습니다.]')
                            show_answer(As[i])
                            st.rerun()
                
          
if __name__ == "__main__":
    #페이지 기본 설정
    st.set_page_config(
        page_icon="./images/cuai_logo.png",
        page_title="CUAI 7기 BASIC Track assignment",
        layout = "wide",
    )
    hide_st_style = """
            <style>
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        #이메일로 로그인
        login_result = login_email() #tuple로 반환 (db에 등록된 이메일인지 여부, 이름, 이메일)


    
    if login_result[0]:
        with st.sidebar:
            #사이드바 크기 조정
            #st.markdown(
            #    """
            #    <style>
            #    [data-testid="stSidebar"][aria-expanded="true"] > div:first-child {
            #        width:250px;
            #    }
            #    </style>
            #    """,
            #    unsafe_allow_html=True,
            #)
            
            
            st.markdown(
                """
                <style>
                [data-testid="StyledFullScreenButton"] {
                    visibility: hidden;
                }
                """,
                unsafe_allow_html=True,
            )
            
            #st.image("./images/cau_cuai_logo.png", use_column_width=True)
            st.image("./images/cuai_logo_transpver.png", use_column_width=True)
            # st.image("./images/cuai_cau_logo.png", use_column_width=True)
            st.write('# 중앙대학교')
            st.write('# 인공지능학회')
            st.write("# **CUAI 7TH**")
            for i in range(3):
                st.write('  ')

            selected = st.selectbox("챕터 선택", [
                'ch02',
                #'ch03',
                #'ch04-1',
                #'ch04-2',
                #'ch05',
                #'ch06',
                #'ch07'
                ])
            #st.markdown('<div style="height: 480px;"></div>', unsafe_allow_html=True)
            
        
        qa = qa_settings.QA[selected]
        deadline = qa["deadline"]
        Qs = qa["Q"]
        As = qa["A"]
        chapter = qa["chapter"]
        chapter_name = qa["chapter_name"]
        name, email = login_result[1:]
        all(deadline, Qs, As, chapter, chapter_name, name, email)

        #상단 오른쪽에 제출했는지 데이터프레임 보여주기
        with col2:
            a,b = st.columns(2)
            with b:
                submit_df(chapter, name, len(Qs))


                
    