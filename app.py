# app.py
import streamlit as st
from streamlit_option_menu import option_menu
from components import checklist, edit_habit, goal_view, review

st.set_page_config(page_title="習慣化トラッカー", layout="centered")
st.title("🌱 習慣化トラッカー")

# ページ切り替え（今は1ページのみ）
# page = st.sidebar.selectbox("ページを選択", ["今日の習慣一覧", "習慣追加・編集", "目的・目標に立ち返り"])
# page = st.sidebar.radio(
#     "📂 ページを選択",
#     ["今日の習慣一覧", "習慣追加・編集", "目的・目標に立ち返り"]
# )
# ChatGPT風サイドバーナビゲーション
with st.sidebar:
    selected = option_menu(
        menu_title="📂 メニュー",
        options=[
          "今日の習慣一覧",
          "習慣追加・編集",
          "目的・目標に立ち返り", 
          "週次・月次の振り返り"
        ],
        icons=["check2", "pencil", "bullseye", "calendar-check"],
        menu_icon="cast",
        default_index=0
    )   

if selected == "今日の習慣一覧":
    checklist.render()
# sidebar ページ選択の中で
elif selected == "習慣追加・編集":
    edit_habit.render()
# sidebar ページ選択の中で
elif selected == "目的・目標に立ち返り":
    goal_view.render()

elif selected == "週次・月次の振り返り":
    review.render()

