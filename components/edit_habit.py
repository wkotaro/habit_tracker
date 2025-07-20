# components/edit_habit.py
import streamlit as st
from utils.file_io import load_data, save_data
import datetime

def render():
    st.header("✏ 習慣と目的の追加")

    data = load_data()

    # 目的登録フォーム
    with st.form("add_goal_form"):
        st.subheader("🎯 新しい目的を追加")
        goal_name = st.text_input("目的名（例：英語力を高めたい）")
        goal_start = st.date_input("開始日", value=datetime.date.today())
        current_goal = st.text_input("現在の目標（例：TOEIC800点）")

        submitted_goal = st.form_submit_button("目的を追加")

        if submitted_goal and goal_name:
            if goal_name not in data["目的一覧"]:
                data["目的一覧"][goal_name] = {
                    "current_goal": current_goal,
                    "completed_goals": [],
                    "start_date": str(goal_start),
                    "habits": []
                }
                save_data(data)
                st.success(f"目的『{goal_name}』を追加しました！")
            else:
                st.warning("その目的は既に存在します")

    st.markdown("---")

    with st.form("add_habit_form"):
        st.subheader("✅ 習慣を追加し、目的に紐づける")
        habit_name = st.text_input("習慣名（例：シャドーイング）")
        habit_category = st.text_input("カテゴリ（例：学習、運動など）")
        notify = st.checkbox("通知を有効にする")
        frequency = st.selectbox("頻度を選択", ["daily", "weekly", "monthly"])
        goal_options = list(data["目的一覧"].keys())
        selected_goal = st.selectbox("紐づける目的を選択", goal_options if goal_options else ["目的が未登録"])
        submitted_habit = st.form_submit_button("習慣を追加")

        if submitted_habit and habit_name and selected_goal in data["目的一覧"]:
            if habit_name not in data["習慣一覧"]:
                data["習慣一覧"][habit_name] = {
                    "log": [],
                    "notify": notify,
                    "category": habit_category,
                    "frequency": frequency
                }
                data["目的一覧"][selected_goal]["habits"].append(habit_name)
                save_data(data)
                st.success(f"習慣『{habit_name}』を目的『{selected_goal}』に追加しました！")
            else:
                st.warning("その習慣は既に存在します")

