# utils/file_io.py
import os
import json

DATA_PATH = "data/habits.json"

# 初期データ構造（目的ベース）
INITIAL_DATA = {
    "目的一覧": {},
    "習慣一覧": {}
}

# データの読み込み／存在しなければ初期化
def load_data():
    if not os.path.exists(DATA_PATH):
        save_data(INITIAL_DATA)
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# データの保存
def save_data(data):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)  # ← ここを追加
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# データを完全に初期化（開発・リセット用）
def reset_data():
    save_data(INITIAL_DATA)

