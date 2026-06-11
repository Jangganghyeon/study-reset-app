import streamlit as st
import pandas as pd
from datetime import datetime
import os

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="Study Reset Dashboard",
    page_icon="📘",
    layout="wide"
)

FILE_NAME = "study_records.csv"

# -----------------------------
# CSS 디자인
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #F7F8FC;
}

.big-title {
    font-size: 42px;
    font-weight: 800;
    color: #2B2D42;
    margin-bottom: 5px;
}

.sub-title {
    font-size: 18px;
    color: #555;
    margin-bottom: 25px;
}

.card {
    background-color: white;
    padding: 22px;
    border-radius: 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.reset-box {
    background: linear-gradient(135deg, #E0F7FA, #F3E5F5);
    padding: 24px;
    border-radius: 18px;
    font-size: 18px;
    font-weight: 600;
    color: #2B2D42;
    margin-top: 15px;
}

.small-text {
    font-size: 14px;
    color: #666;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 데이터 함수
# -----------------------------
def load_data():
    if os.path.exists(FILE_NAME):
        return pd.read_csv(FILE_NAME)
    return pd.DataFrame(columns=[
        "날짜", "과목", "원래 계획량", "실제 수행량", "달성률",
        "계획 수정 이유", "공부 전 감정", "공부 후 감정", "공부 시간", "메모"
    ])

def save_data(df):
    df.to_csv(FILE_NAME, index=False, encoding="utf-8-sig")

def get_reset_message(reason, achievement_rate, emotion_before, emotion_after):
    if achievement_rate >= 100:
        return "오늘은 계획을 충분히 달성했습니다. 이 흐름을 그대로 유지하면 됩니다."

    if reason == "수면 부족":
        return "수면이 부족한 날에는 계획을 줄이는 것이 실패가 아니라 회복 전략입니다."

    if reason == "시간 부족":
        return "시간이 부족했다면 핵심 과목만 남기는 선택이 더 현실적입니다."

    if reason == "난이도 높음":
        return "난이도가 높아 속도가 느려진 것은 자연스러운 일입니다. 오늘은 이해한 범위를 기록하는 것이 중요합니다."

    if reason == "컨디션 저하":
        return "컨디션이 낮은 날에도 일부를 해냈다면 학습 흐름은 유지된 것입니다."

    if emotion_before in ["불안함", "짜증남", "무기력함"] and emotion_after in ["괜찮음", "뿌듯함"]:
        return "공부 전 감정은 좋지 않았지만, 공부 후 감정이 회복되었습니다. 오늘의 공부는 감정 리셋 효과가 있었습니다."

    return "계획을 완벽히 지키지 못했더라도 기록하고 조정했다면 흐름은 이어진 것입니다."

# -----------------------------
# 데이터 불러오기
# -----------------------------
df = load_data()

# -----------------------------
# 상단 제목
# -----------------------------
st.markdown('<div class="big-title">📘 Study Reset Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">공부 계획 이탈을 실패가 아닌 조정으로 기록하는 학습 리셋 웹사이트</div>',
    unsafe_allow_html=True
)

# -----------------------------
# 상단 요약 카드
# -----------------------------
total_records = len(df)
total_time = int(df["공부 시간"].sum()) if not df.empty else 0
avg_achievement = round(df["달성률"].mean(), 1) if not df.empty else 0

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("누적 기록 수", f"{total_records}개")

with col2:
    st.metric("누적 공부 시간", f"{total_time}분")

with col3:
    st.metric("평균 계획 달성률", f"{avg_achievement}%")

st.divider()

# -----------------------------
# 탭 구성
# -----------------------------
tab1, tab2, tab3 = st.tabs(["📝 오늘 기록하기", "📊 나의 패턴 분석", "🔁 리셋 조언"])

# -----------------------------
# 탭 1: 기록 입력
# -----------------------------
with tab1:
    st.subheader("오늘의 공부 기록")

    with st.form("study_form"):
        c1, c2 = st.columns(2)

        with c1:
            subject = st.selectbox(
                "과목",
                ["국어", "영어", "수학", "물리", "화학", "생명"]
            )

            original_amount = st.number_input(
                "원래 계획량",
                min_value=0,
                max_value=100,
                value=10,
                help="예: 10페이지, 20문제처럼 숫자만 입력"
            )

            actual_amount = st.number_input(
                "실제 수행량",
                min_value=0,
                max_value=100,
                value=8,
                help="예: 실제로 8페이지를 했다면 8 입력"
            )

            study_time = st.number_input(
                "공부 시간(분)",
                min_value=0,
                max_value=600,
                value=60
            )

        with c2:
            reason = st.selectbox(
                "계획 수정 이유",
                ["수정 없음", "수면 부족", "시간 부족", "난이도 높음", "컨디션 저하", "다른 과목 우선", "기타"]
            )

            emotion_before = st.selectbox(
                "공부 전 감정",
                ["괜찮음", "피곤함", "불안함", "짜증남", "무기력함", "자신감 있음"]
            )

            emotion_after = st.selectbox(
                "공부 후 감정",
                ["괜찮음", "피곤함", "불안함", "짜증남", "무기력함", "뿌듯함"]
            )

            memo = st.text_area(
                "한 줄 메모",
                placeholder="예: 원래 계획보다 줄였지만 흐름은 유지했다."
            )

        submitted = st.form_submit_button("오늘 기록 저장하기")

    if submitted:
        if original_amount == 0:
            achievement_rate = 0
        else:
            achievement_rate = round((actual_amount / original_amount) * 100, 1)

        new_record = pd.DataFrame([{
            "날짜": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "과목": subject,
            "원래 계획량": original_amount,
            "실제 수행량": actual_amount,
            "달성률": achievement_rate,
            "계획 수정 이유": reason,
            "공부 전 감정": emotion_before,
            "공부 후 감정": emotion_after,
            "공부 시간": study_time,
            "메모": memo
        }])

        df = pd.concat([df, new_record], ignore_index=True)
        save_data(df)

        st.success("기록이 저장되었습니다.")

        message = get_reset_message(reason, achievement_rate, emotion_before, emotion_after)
        st.markdown(f'<div class="reset-box">🔁 {message}</div>', unsafe_allow_html=True)

    st.subheader("최근 기록")

    if df.empty:
        st.info("아직 기록이 없습니다.")
    else:
        st.dataframe(df.tail(10), use_container_width=True)

# -----------------------------
# 탭 2: 패턴 분석
# -----------------------------
with tab2:
    st.subheader("나의 학습 패턴 분석")

    if df.empty:
        st.info("분석할 기록이 아직 없습니다.")
    else:
        c1, c2 = st.columns(2)

        with c1:
            st.markdown("#### 과목별 누적 공부 시간")
            subject_time = df.groupby("과목")["공부 시간"].sum()
            st.bar_chart(subject_time)

        with c2:
            st.markdown("#### 과목별 평균 달성률")
            subject_rate = df.groupby("과목")["달성률"].mean()
            st.bar_chart(subject_rate)

        st.markdown("#### 계획 수정 이유 분포")
        reason_count = df["계획 수정 이유"].value_counts()
        st.bar_chart(reason_count)

        most_changed_reason = df["계획 수정 이유"].value_counts().idxmax()
        weakest_subject = df.groupby("과목")["달성률"].mean().idxmin()

        st.markdown(f"""
        <div class="card">
        <h4>자동 분석 결과</h4>
        <p>가장 자주 나타난 계획 수정 이유는 <b>{most_changed_reason}</b>입니다.</p>
        <p>평균 달성률이 가장 낮은 과목은 <b>{weakest_subject}</b>입니다.</p>
        <p class="small-text">이 결과를 바탕으로 다음 계획을 세울 때 해당 과목의 계획량을 조금 더 현실적으로 조정할 수 있습니다.</p>
        </div>
        """, unsafe_allow_html=True)

# -----------------------------
# 탭 3: 리셋 조언
# -----------------------------
with tab3:
    st.subheader("상황별 리셋 조언")

    situation = st.selectbox(
        "현재 상황을 선택하세요.",
        [
            "계획을 다 못 지켰을 때",
            "공부하기 전부터 불안할 때",
            "계산 실수 때문에 짜증날 때",
            "수면 부족으로 집중이 안 될 때",
            "한 과목이 계속 밀릴 때"
        ]
    )

    advice = {
        "계획을 다 못 지켰을 때": [
            "오늘 한 양을 먼저 기록합니다.",
            "못 한 양보다 유지한 흐름에 집중합니다.",
            "내일 계획에 오늘 못 한 것을 전부 넣지 말고 핵심만 옮깁니다."
        ],
        "공부하기 전부터 불안할 때": [
            "처음 목표를 20분짜리 작은 단위로 줄입니다.",
            "가장 부담이 적은 과목부터 시작합니다.",
            "시작 후 감정이 바뀌는지 기록합니다."
        ],
        "계산 실수 때문에 짜증날 때": [
            "실수한 문제를 다시 풀기 전에 실수 유형을 먼저 적습니다.",
            "부호, 분수, 조건 누락 중 어디에서 무너졌는지 표시합니다.",
            "같은 유형이 반복되면 풀이 속도를 줄이는 구간을 정합니다."
        ],
        "수면 부족으로 집중이 안 될 때": [
            "새로운 고난도 문제보다 복습 위주로 전환합니다.",
            "계획량을 줄여도 기록은 남깁니다.",
            "컨디션이 낮은 날의 최소 기준을 따로 정합니다."
        ],
        "한 과목이 계속 밀릴 때": [
            "그 과목의 계획량이 과한지 확인합니다.",
            "매일 10분짜리 최소 단위로 바꿉니다.",
            "완료 경험을 먼저 만든 뒤 양을 늘립니다."
        ]
    }

    st.markdown('<div class="reset-box">오늘의 리셋 전략</div>', unsafe_allow_html=True)

    for item in advice[situation]:
        st.write(f"- {item}")

    st.warning("이 웹사이트의 목표는 완벽한 계획 수행이 아니라, 공부 흐름을 끊지 않는 것입니다.")
