# components/goal_view.py
import streamlit as st
from utils.file_io import load_data, save_data
import datetime

def render():
    st.header("🎯 目的と現在の目標一覧")

    data = load_data()

    if not data["目的一覧"]:
        st.info("現在登録されている目的はありません")
        return

    for goal_name, goal_info in data["目的一覧"].items():
        current = goal_info.get("current_goal", "未設定")

        # 削除フラグが立っている目的は表示しない
        if goal_info.get("deleted", False):
            continue

        with st.expander(goal_name):
            st.markdown(f"**現在の目標：** {current if current else '未設定'}")

            # 1. 目標達成処理
            if current:
                if st.button(f"✅ 『{current}』を達成済みにする", key=f"complete_{goal_name}"):
                    today = datetime.date.today().isoformat()
                    goal_info.setdefault("completed_goals", []).append({
                        "goal": current,
                        "date": today
                    })
                    goal_info["current_goal"] = ""
                    save_data(data)
                    st.success("目標を達成済みにしました。新しい目標を入力してください。")

            # 2. 目標編集機能
            new_goal = st.text_input("✏ 新しい目標（上書きまたは更新）", value=current, key=f"edit_{goal_name}")
            if st.button("💾 目標を更新する", key=f"save_{goal_name}"):
                goal_info["current_goal"] = new_goal
                save_data(data)
                st.success("目標を更新しました")

            # 3. 目標削除（deleted フラグを立てる）
            if st.button("🗑 現在の目標を削除", key=f"delete_{goal_name}"):
                goal_info["deleted"] = True
                save_data(data)
                st.warning("現在の目標を削除しました")

            # 過去の目標履歴
            if goal_info.get("completed_goals"):
                st.markdown("**過去に達成した目標：**")
                for item in goal_info["completed_goals"]:
                    st.markdown(f"- {item['goal']}（{item['date']}）")

            st.markdown("---")
            if goal_info.get("habits"):
                st.markdown("**紐づく習慣：**")
                for habit in goal_info["habits"]:
                    st.markdown(f"- {habit}")

