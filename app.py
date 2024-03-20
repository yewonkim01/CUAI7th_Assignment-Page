import streamlit as st
import qa_settings
from DB_class import DB
from email_info import data

import pytz
from datetime import datetime
import time
from notice_tab import display_notice_tab


if 'notice' not in st.session_state:
    st.session_state['notice'] = """
            * 문제는 모두 주관식이며, 제한시간은 없습니다.<br><br>
            * Basic Track 퀴즈 참여는 학회 출석 요건 중 하나입니다. 정해진 기간 안에 꼭 응시해주세요.<br><br>
            * 문제 풀이 결과는 학회 수료와 무관하니, 정답 유무에 관계없이 개념 확인 용도로 퀴즈를 응시해주세요.<br><br>
            * 퀴즈 응시 기간이 지나면, 퀴즈를 응시하실 수 없고 자동으로 과제 미제출로 반영됩니다.
            """

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
        for i in range(3):
                st.write('  ')

        st.write(st.session_state['notice'], unsafe_allow_html=True)
        return (False,)

#정답출력 함수
def show_answer(A:str):    
    ans_css = """
        <style>
            .ans-rounded-box {
                border-radius: 10px;
                background-color: #45435A;
                padding: 20px;
                height: 250px;
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
    st.markdown(f'<div class="ans-rounded-box" style="font-size: 15px;">{A}</div>', unsafe_allow_html=True)


def all(tabs, col2, db, deadline, Qs:list, As:list, submits:list, kst):
    '''
    db: 데이터베이스
    Qs: 해당 주차 문제 담긴 리스트
    As: 해당 주차 정답 담긴 리스트
    chapter: 챕터    ex)ch01 (db에 저장되는 collection 이름)
    chapter_name: 챕터이름 ex)차원축소
    name: 학회원 이름
    email: 학회원 이메일
    '''

    
    if 'deadline_passed' not in st.session_state:
        st.session_state.deadline_passed = False

    now = datetime.now(kst)
    if now > deadline:
        st.session_state.deadline_passed = True

    
    

    #존재하는 tab수만큼 반복문 돌리면서 화면 구성
    for i in range(1, len(tabs)):
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
                            height: 590px;
                            margin-right:10px;
                        }
                    </style>
                """
                # CSS 적용
                st.markdown(css, unsafe_allow_html=True)
                #Qs는 문제가 담긴 리스트  
                q = Qs[i-1]

                # 둥근 사각형 만들어서 안에 문제 적기
                st.markdown(f'<div class="rounded-box"style="font-size: 15px;">{q}</div>', unsafe_allow_html=True)

            # 오른쪽 답변/정답 열
            with col2:
                st.write('\n')

                if f'num{i}_ans' not in st.session_state:
                    st.session_state[f'num{i}_ans'] = db.submitted_answer(i)

                #submitted_ans = db.submitted_answer(i)

                answer = st.text_area(" ", key = f'num{i}_ans', height=200,
                                      placeholder="답안을 작성해 주세요.",
                                      #value=st.session_state[f'num{i+1}_ans']
                                      )
                


                a,b,c,d = st.columns(4)
                with a:
                    # 제출하기 button
                    button = st.button("제출하기",
                                       key=f"button{i+1}",
                                       disabled = (st.session_state.num_submitted[i-1]) or (now > deadline))

                with d:
                    # # 제출된 답변 있으면 정답화면 바로 보이게/
                    #submits = db.submitted_check(Qs) #submits = [1,0,1,1,1]
                    if submits[i-1]:
                        st.markdown(' :green[☑ 제출되었습니다.]')
                        
                if submits[i-1]: show_answer(As[i-1])

                # 제출된 답변 없으면 <제출하기> 버튼 눌러야 정답확인 가능 
                if button:
                    now = datetime.now(kst)
                    if now > deadline:
                        st.session_state.deadline_passed = True
                    #DEADLINE 기능 추가: 설정된 deadline 지나면 제출할 수 없음.
                    st.session_state.button_pressed = True
                    

                    #if button_now > deadline:
                    if st.session_state.deadline_passed:
                        st.error('과제 제출 기한이 지나 제출할 수 없습니다.')
                    else:
                        # 이미 제출했는데 버튼 또 누르면(재제출)
                        if submits[i-1]:
                            print(submits)
                            pass
                            # db에만 답변 저장
                            #st.session_state.return_num = i
                            #db.save_db(i, answer)
                            #st.rerun()
                            
                        # # 처음 제출이면
                        # 제출문구 띄우고 답변 보여주기
                        else:
                            with d: st.markdown(' :green[☑ 제출되었습니다.]')
                            show_answer(As[i-1])
                            st.session_state.return_num = i
                            st.session_state.num_submitted[i-1] = 1
                            db.save_db(i, answer)
                            #st.rerun()

def deadline_passed_all(tabs, col2, db, deadline, Qs:list, As:list, submits:list, kst): 
    #존재하는 tab수만큼 반복문 돌리면서 화면 구성
    for i in range(1, len(tabs)):
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
                            height: 590px;
                            margin-right:10px;
                        }
                    </style>
                """
                # CSS 적용
                st.markdown(css, unsafe_allow_html=True)
                #Qs는 문제가 담긴 리스트  
                q = Qs[i-1]

                # 둥근 사각형 만들어서 안에 문제 적기
                st.markdown(f'<div class="rounded-box"style="font-size: 15px;">{q}</div>', unsafe_allow_html=True)

            # 오른쪽 답변/정답 열
            with col2:
                st.write('\n')
                num_answer = {}
                num_answer[f'num{i}_ans'] = db.submitted_answer(i)

                answer = st.text_area(" ", key = f'num{i}_ans', height=200,
                                      placeholder="답안을 작성해 주세요.",
                                      value=num_answer[f'num{i}_ans']
                                      )
                


                a,b,c,d = st.columns(4)
                with a:
                    # 제출하기 button
                    now = datetime.now(kst)
                    button = st.button("제출하기",
                                       key=f"button{i+1}",
                                       disabled = now > deadline)

                with d:
                    # # 제출된 답변 있으면 정답화면 바로 보이게/
                    submits = db.submitted_check(Qs) #submits = [1,0,1,1,1]
                    if submits[i-1]:
                        st.markdown(' :green[☑ 제출되었습니다.]')
                        
                if submits[i-1]: show_answer(As[i-1])  
          
if __name__ == "__main__":
    print('page reloaded')
    #페이지 기본 설정
    st.set_page_config(
        page_icon="./images/cuai_logo.png",
        page_title="CUAI 7기 BASIC Track assignment",
        layout = "wide",
    ) 

    st.markdown(
    """
    <style>
    .stApp {
        margin-top: -30px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    hide_st_style = """
            <style>
            header {visibility: hidden;}
            </style>
            """
    st.markdown(hide_st_style, unsafe_allow_html=True)

    st.write('<style>div.block‑container{padding‑top:2rem;}</style>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        #이메일로 로그인
        login_result = login_email() #tuple로 반환 (db에 등록된 이메일인지 여부, 이름, 이메일)

    if login_result[0]:
        with st.sidebar:
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

            chapter_options = [
                'ch02',
                'ch03',
                #'ch04-1',
                #'ch04-2',
                #'ch05',
                #'ch06',
                #'ch07'
            ]
            selected = st.selectbox("챕터 선택", 
                                    chapter_options,
                                    index = 1)
            
        
        qa = qa_settings.QA[selected]
        deadline = qa["deadline"]
        Qs = qa["Q"]
        As = qa["A"]
        chapter = qa["chapter"]
        chapter_name = qa["chapter_name"]

        name, email = login_result[1:]

        db = DB(chapter, name)

        kst = pytz.timezone('Asia/Seoul')
        now = datetime.now(kst)
        deadline = deadline.astimezone(kst)

        if now < deadline:
            if 'return_num' not in st.session_state:
                st.session_state.return_num = ''

            if 'num_submitted' not in st.session_state:
                submits = db.submitted_check(Qs)  #submits = [1,0,1,1,1]
                st.session_state.num_submitted = submits

            if 'button_pressed' not in st.session_state:
                st.session_state.button_pressed = False
            
            if 'FINAL_SUBMIT' not in st.session_state:
                st.session_state['FINAL_SUBMIT'] = db.check_FINAL_SUBMIT()

            if 'submitted' not in st.session_state:
                st.session_state.submitted = False

            if st.session_state['FINAL_SUBMIT']:
                st.session_state.submitted = True

        

        # 페이지 서브헤더 제목 설정
        st.subheader(f"[Chapter{chapter[2:]}] {chapter_name}")
        
        #문제들을 tab으로 구현
        tabs = st.tabs(['notice']+[f'Q{i}' for i in range(1, len(Qs)+1)])
        
        
        if now > deadline:
            deadline_passed_all(tabs, col2, db, deadline, Qs, As, st.session_state.num_submitted, kst)
        else:
            all(tabs, col2, db, deadline, Qs, As, st.session_state.num_submitted, kst)
            print(st.session_state.num_submitted)


        #상단 오른쪽에 제출했는지 데이터프레임 보여주기
        with col2:
            a,b = st.columns([1,4])
            with b:
                if now > deadline:
                    v = {f'Q{i}': db.check_db_submitted(f"Q{i}") for i in range(1, len(Qs)+1)}
                    print(v)
                    a = db.deadline_passed_submit_df(v)
                    fs = db.check_FINAL_SUBMIT()
                    display_notice_tab(tabs, deadline, True, a, fs)

                else:
                    if 'value' not in st.session_state:
                        st.session_state.value = {f'Q{i}': db.check_db_submitted(f"Q{i}") for i in range(1, len(Qs)+1)}
                    else:
                        if st.session_state.return_num:
                            st.session_state.value[f'Q{st.session_state.return_num}'] = 'O'
                    db.submit_df()                
                    display_notice_tab(tabs, deadline, st.session_state.deadline_passed, st.session_state['submitted'], None)
                    
                
                
        
                
                
