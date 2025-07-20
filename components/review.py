# components/review.py
import streamlit as st
from utils.file_io import load_data, save_data
import datetime
import json
from collections import defaultdict
import os

REVIEW_FILE = "data/reviews.json"

# 初期化と読み込み
def load_reviews():
    if not os.path.exists(REVIEW_FILE):
        return {}
    try:
        with open(REVIEW_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_reviews(reviews):
    os.makedirs(os.path.dirname(REVIEW_FILE), exist_ok=True)
    with open(REVIEW_FILE, "w", encoding="utf-8") as f:
        json.dump(reviews, f, indent=2, ensure_ascii=False)

def render():
    st.header("📝 週次・月次の振り返り")

    today = datetime.date.today()
    year_week = today.strftime("%Y-W%U")
    year_month = today.strftime("%Y-%m")

    tab = st.radio("振り返りの対象期間", ["週次", "月次"])
    key = year_week if tab == "週次" else year_month

    reviews = load_reviews()
    data = load_data()

    st.subheader(f"{tab}振り返り（{key}）")
    comment = st.text_area("今週／今月の気づき・反省・よかったこと", value=reviews.get(key, ""))

    if st.button("保存"):
        reviews[key] = comment
        save_reviews(reviews)
        st.success(f"{tab}の振り返りを保存しました ✅")

    st.markdown("---")
    st.subheader("📊 今週／今月の達成サマリー")

    # 対象期間の判定関数
    def is_in_period(date_str):
        try:
            d = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
            if tab == "週次":
                return d.isocalendar()[1] == today.isocalendar()[1] and d.year == today.year
            else:
                return d.month == today.month and d.year == today.year
        except:
            return False

    goal_summary = defaultdict(list)

    for goal_name, goal_data in data.get("目的一覧", {}).items():
        for habit_name in goal_data.get("habits", []):
            habit = data["習慣一覧"].get(habit_name)
            if habit:
                logs = [d for d in habit.get("log", []) if is_in_period(d)]
                if logs:
                    goal_summary[goal_name].append((habit_name, len(logs), goal_data.get("goals", [])))

    if not goal_summary:
        st.info("今週／今月の達成習慣はまだ記録されていません。")
    else:
        for goal_name, habits in goal_summary.items():
            st.markdown(f"### 🎯 {goal_name}")
            goal_details = habits[0][2] if habits else []
            if goal_details:
                st.caption("目標：")
                for g in goal_details:
                    st.markdown(f"- {g}")
            for habit_name, count, _ in habits:
                st.markdown(f"- ✅ {habit_name}：{count}回")

    st.markdown("---")
    st.subheader("📖 保存された振り返り一覧")

    if reviews:
        sorted_reviews = dict(sorted(reviews.items(), reverse=True))
        for period, text in sorted_reviews.items():
            with st.expander(f"📅 {period}"):
                st.markdown(text if text else "_(記録なし)_")
    else:
        st.info("まだ保存された振り返りがありません。")

