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

                with col1: st.markdown('📄문제수 8개')
                with col2: st.markdown('⏱️제한 시간 없음')

                with col1: st.write(' ')
                with col2: st.write(' ')
                
                
                deadline = deadline.strftime(f"%Y.%m.%d %H:%M:%S")
                with col1: st.markdown('🗓️응시 기간')
                with col2: st.markdown(f'~ {deadline[2:]}')
                success = """
                    <style>
                        .success-box {
                            border: 2px solid #007355;
                            border-radius: 10px;
                            padding: 15px;
                            
                            height: 85px;
                            #width: 500px;
                            #margin-right:10px;
                            #margin-bottom:20px;
                            #overflow-y: auto;
                            color: #ffffff;
                        }
                        .bold-text {
                            font-weight: bold; /* 텍스트를 볼드체로 지정 */
                        }
                        .green-text {
                            color: #007355; /* 텍스트를 초록색으로 지정 */
                        }
                    </style>
                """

                fail = """
                    <style>
                        .fail-box {
                            border: 2px solid #A43232;
                            border-radius: 10px;
                            padding: 15px;

                            height: 85px;
                            #width: 500px;
                            #margin-right:10px;
                            #margin-bottom:20px;
                            #overflow-y: auto;
                            color: #ffffff;
                        }
                        .bold-text {
                            font-weight: bold; /* 텍스트를 볼드체로 지정 */
                        }
                        .red-text {
                            color: #A43232; /* 텍스트를 초록색으로 지정 */
                        }
                    </style>
                """
                # CSS 적용 마크다운
                st.markdown(success, unsafe_allow_html=True)

                # CSS 적용 마크다운
                st.markdown(fail, unsafe_allow_html=True)


                if submitted:
                    comment = f"""✅ <span class="bold-text green-text">퀴즈 응시 완료</span><br>
                            {'&nbsp;' * 8}<span class="green-text">{st.session_state['FINAL_SUBMIT']} 제출 완료</span>"""
                    box = "success"
                    
                elif not submitted:
                    if deadline_passed:
                        comment = f"""🚫 <span class="bold-text red-text">퀴즈 미제출</span><br>
                                {'&nbsp;' * 8}응시 기간이 지나 응시할 수 없습니다."""
                        box = "fail"
                    
                    else:
                        comment = f"""<span class="bold-text green-text">💡퀴즈 제출 전입니다.</span><br>
                                {'&nbsp;' * 8}응시 기간 안에 제출을 완료해주세요."""
                        box = "success"

                # 둥근 사각형 안에 글씨 출력
                st.markdown(f'<div class="{box}-box">{comment}</div>', unsafe_allow_html=True)

                for i in range(10):
                     st.write(' ')
                
                st.markdown('※ 퀴즈 응시 중 문제가 발생하면 즉시 "CUAI 카카오톡 채널"로 문의바랍니다.')


        