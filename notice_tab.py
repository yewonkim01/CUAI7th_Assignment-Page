import streamlit as st

def display_notice_tab(tabs, deadline, deadline_passed, submitted):
    box = ""
    with tabs[0]:
            
            st.write(' ')
            a,b = st.columns(2)
            with a: 
                col1,col2,col3 = st.columns(3)
                #with col1: st.write(' ')
                #with col2: st.write(' ')

                with col1: st.markdown('<span style="font-weight:bold;">📄문제수 8개</span>', unsafe_allow_html=True)
                with col2: st.markdown('<span style="font-weight:bold;">⏱️제한 시간 없음</span>', unsafe_allow_html=True)

                with col1: st.write(' ')
                with col2: st.write(' ')
                
                
                deadline = deadline.strftime(f"%Y.%m.%d %H:%M:%S")
                with col1: st.markdown('<span style="font-weight:bold;">🗓️응시 기간</span>', unsafe_allow_html=True)
                with col2: st.markdown(f'<span style="font-weight:bold;">~ {deadline[2:]}</span>', unsafe_allow_html=True)
                success = """
                    <style>
                        .success-box {
                            border-radius: 10px;
                            background-color: #C4DDC1;
                            padding: 20px;
                            height: 80px;
                            #width: 500px;
                            margin-right:10px;
                            margin-bottom:20px;
                            overflow-y: auto;
                            color: #007355;
                        }
                        .bold-text {
                            font-weight: bold; /* 텍스트를 볼드체로 지정 */
                        }
                    </style>
                """

                fail = """
                    <style>
                        .fail-box {
                            border-radius: 10px;
                            background-color: #EBB1B0;
                            padding: 20px;
                            height: 80px;
                            #width: 500px;
                            margin-right:10px;
                            margin-bottom:20px;
                            overflow-y: auto;
                            color: #A40000;
                        }
                        .bold-text {
                            font-weight: bold; /* 텍스트를 볼드체로 지정 */
                        }
                    </style>
                """
                # CSS 적용 마크다운
                st.markdown(success, unsafe_allow_html=True)

                # CSS 적용 마크다운
                st.markdown(fail, unsafe_allow_html=True)


                if submitted:
                    comment = f"""✅ <span class="bold-text">테스트 응시 완료</span><br>
                            {'&nbsp;' * 8}{st.session_state['FINAL_SUBMIT']} 제출 완료"""
                    box = "success"
                    
                elif not submitted:
                    if deadline_passed:
                        comment = f"""🚫 <span class="bold-text">퀴즈 미제출</span><br>
                                {'&nbsp;' * 8}응시 기간이 지나 응시할 수 없습니다."""
                        box = "fail"
                    
                    else:
                        comment = f"""<span class="bold-text">💡테스트를 응시해주세요.</span><br>"""
                        box = "success"

                # 둥근 사각형 안에 글씨 출력
                st.markdown(f'<div class="{box}-box">{comment}</div>', unsafe_allow_html=True)

                for i in range(10):
                     st.write(' ')
                
                st.markdown('※ 과제 제출에 문제가 발생하면 즉시 "CUAI 카카오톡 채널"로 문의바랍니다.')


        