import streamlit as st
import pandas as pd
import numpy as np




# 페이지 기본 설정
st.set_page_config(
    #page_icon=""
    page_title="CUAI 7기 BASIC Track assignment",
    layout = "wide",
)



def show_ans(submit, A):
    if submit:
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
        # CSS를 적용하기 위해 markdown 사용
        st.markdown(ans_css, unsafe_allow_html=True)  

        # 둥근 사각형 안에 글씨 출력
        st.markdown(f'<div class="ans-rounded-box">{A}</div>', unsafe_allow_html=True)


# 페이지 헤더, 서브헤더 제목 설정
st.subheader("[Chapter6] 차원축소")

tab1, tab2, tab3, tab4, tab5 = st.tabs(['Q1', 'Q2', 'Q3', 'Q4', 'Q5'])
tabs = [tab1, tab2, tab3, tab4, tab5]
submits = [False]*len(tabs)
qs = ["Q. 신경망을 이용하여 분류 문제를 해결할 때 회귀문제를 해결할 때와 어떻게 달라지나요?",
      "Q. 두 번째 문제",
      "Q. 세 번째 문제",
      "Q. 네 번째 문제",
      "Q. 다섯 번째 문제"]
As = [
    """출력층 부분이 달라진다.<br>
            분류 문제를 풀 경우에는 출력층의 활성화 함수를 softmax로 그리고 노드의 개수는 분류하는 class의 개수로 설정해야한다.<br>
                회귀 문제를 풀 경우에는 출력층의 활성화 함수를 항등함수로 그리고 노드의 개수는 한 개로 설정해야한다.""",
                """가나다""",
                """가나다""",
                """가나다""",
                """가나다""",
]

for i in range(len(tabs)):
    with tabs[i]:
        # 텍스트 입력 및 저장
        col1, col2 = st.columns(2)

        with col1:
            st.write("")
            css = """
                <style>
                    .rounded-box {
                        border-radius: 10px;
                        background-color: #45435A;
                        padding: 20px;
                        height: 700px;
                        margin-right:10px;
                    }
                </style>
            """
            # CSS를 적용하기 위해 markdown 사용
            st.markdown(css, unsafe_allow_html=True)  

            q = qs[i]

            # 둥근 사각형 안에 글씨 출력
            st.markdown(f'<div class="rounded-box">{q}</div>', unsafe_allow_html=True)



        with col2:
            st.write('\n')
            answer = st.text_area("", key = f"ans{i+1}", height=200, placeholder="답안을 작성해 주세요.")
            button = st.button("제출하기", key=f"button{i+1}")


            if len(answer.strip()) >= 10:
                if button:
                    submits[i] = True
                    st.markdown(' :green[☑ 제출되었습니다.]')
                    show_ans(submits[i], As[i])
                    q,w,e,r,t = st.columns(5)
                    with t:
                        st.button("다음 문제로 이동>")
                    
            else:
                st.markdown('10자 이상 작성해주세요.')
            

        





