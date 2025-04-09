import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

DATA_FOLDER = "rate_data"  # CSVファイルを保存するフォルダ
os.makedirs(DATA_FOLDER, exist_ok=True)  # フォルダがなければ作成

def get_file_path(game_name):
    """ゲーム名からCSVファイルのパスを取得"""
    return os.path.join(DATA_FOLDER, f"{game_name}.csv")

def initialize_csv(file_path):
    """CSVファイルが存在しない場合、空のデータを作成"""
    if not os.path.exists(file_path):
        df = pd.DataFrame({"Date": [], "Race Number": [], "Rate": []})
        df.to_csv(file_path, index=False)

def load_data(file_path):
    """CSVファイルからデータを読み込む"""
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame({"Date": [], "Race Number": [], "Rate": []})

def save_data(df, file_path):
    """データをCSVに保存"""
    df.to_csv(file_path, index=False)

def plot_graph(df):
    """レート推移のグラフを描画"""
    if df.empty:
        st.write("データがありません。")
        return

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(df["Race Number"], df["Rate"], marker='o', linestyle='-', color='b', label="Rate Progression")

    ax.set_xlabel("Race Number (Date)")
    ax.set_ylabel("Rate")
    ax.set_title("Rate Progression Over Time")
    race_number = df["Race Number"].astype(int)
    ax.set_xticks(race_number)
    ax.set_xticklabels([f"{num}\n({date})" for num, date in zip(race_number, df["Date"])], rotation=45, ha="right")
    ax.legend()
    ax.grid(True)

    st.pyplot(fig)

# Streamlit UI
st.title("ゲーム別レート記録アプリ")
st.write("記録したいゲームのCSVファイルを選択してください。")

# **ゲーム名の入力**
game_name = st.text_input("ゲーム名を入力（例: マリオカート, スプラトゥーン）")
if game_name:
    file_path = get_file_path(game_name)
    initialize_csv(file_path)
    df = load_data(file_path)

    # **横並びレイアウト**
    col1, col2 = st.columns([3, 2])  # 左: 60% 右: 40% の比率

    with col1:
        # **1️⃣ レートを新規追加**
        st.subheader("レートを新規追加")
        new_rate = st.number_input("レートを入力:", min_value=0, step=1)
        if st.button("追加"):
            today = datetime.today().strftime("%Y-%m-%d")
            new_race_number = len(df) + 1

            new_data = pd.DataFrame({"Date": [today], "Race Number": [new_race_number], "Rate": [new_rate]})
            df = pd.concat([df, new_data], ignore_index=True)

            save_data(df, file_path)
            st.success(f"{game_name} のレートを追加しました！")
            st.rerun()

        # **2️⃣ レート推移グラフ**
        st.subheader("レートの推移グラフ")
        plot_graph(df)

    with col2:
        # **3️⃣ レートデータのテーブル**
        if not df.empty:
            st.subheader("レートデータ")
            edited_df = st.data_editor(df, num_rows="dynamic")  # Streamlitのエディタで編集可能にする

            if st.button("変更を保存"):
                save_data(edited_df, file_path)
                st.success("データを更新しました！")
                st.rerun()


