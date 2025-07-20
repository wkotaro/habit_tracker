# components/checklist.py
import streamlit as st
import datetime
from utils.file_io import load_data, save_data

def render():
    st.header("✅ 今日の習慣一覧")

    today = str(datetime.date.today())
    data = load_data()

    if "習慣一覧" not in data:
        st.warning("習慣データがありません。習慣を追加してください。")
        return

    updated = False

    for habit_name, habit_info in data["習慣一覧"].items():
        log = habit_info.get("log", [])
        checked = today in log
        new_value = st.checkbox(habit_name, value=checked)

        if new_value and today not in log:
            habit_info.setdefault("log", []).append(today)
            updated = True
        elif not new_value and today in log:
            habit_info["log"].remove(today)
            updated = True

    if updated:
        save_data(data)
        st.success("保存しました ✅")

