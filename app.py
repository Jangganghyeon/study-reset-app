import streamlit as st

st.title("공부 감정·계획 리셋 웹사이트")

st.write("오늘의 공부 상태를 기록하고, 계획이 틀어졌을 때 다시 리셋하는 웹사이트입니다.")

subject = st.selectbox(
    "오늘 공부한 과목을 선택하세요.",
    ["국어", "영어", "수학", "물리", "화학", "생명"]
)

emotion = st.selectbox(
    "지금 감정은 어떤가요?",
    ["괜찮음", "피곤함", "불안함", "짜증남", "뿌듯함", "자신감 있음"]
)

study_time = st.number_input(
    "공부 시간은 몇 분인가요?",
    min_value=0,
    max_value=600,
    value=60
)

if st.button("기록하기"):
    st.success(f"{subject} {study_time}분 공부 기록 완료!")
    st.write(f"현재 감정: {emotion}")
