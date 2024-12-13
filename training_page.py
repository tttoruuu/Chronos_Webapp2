import streamlit as st
from openai import OpenAI
import openai
import os
from initializers import get_firestore_client
from google.cloud import firestore
import re


def switch_page(page_name):
    st.session_state["current_page"] = page_name

def training_page():
    try:#Firestoreからデータを参照
        db = get_firestore_client()  # クライアントを関数内で取得
    except RuntimeError as e:
        st.error(f"Firestore クライアントの初期化エラー: {e}")
        return

    st.title("今日のやること")

    uid = st.session_state["user"]["uid"]
    user_ref = db.collection("users").document(uid)
    user_data = user_ref.get().to_dict()
    

    # Firestoreの既存タスクを取得
    task_ref = db.collection("tasks").document(uid)
    task_data = task_ref.get().to_dict()

    def generate_tasks(prompt):
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt},
            ],
        )
        tasks = response.choices[0].message.content.strip().split("\n")
        # 正規表現で番号付きタスクを抽出し、次の番号までの内容を含める
        task_list = []
        current_task = []
        for line in tasks:
            if re.match(r"^\d+\.\s", line.strip()):  # 番号で始まる行
                if current_task:  # 現在のタスクを保存
                    task_list.append(" ".join(current_task).strip())
                current_task = [line.strip()]
            else:
                if current_task:  # 番号が付いていない行を現在のタスクに追加
                    current_task.append(line.strip())
        if current_task:  # 最後のタスクを保存
            task_list.append(" ".join(current_task).strip())
        return task_list

    if task_data:
        tasks = task_data.get("tasks", [])
        st.subheader("習慣化のリスト")
        st.text("まずこれは前回から引き継いでいるリストだよ。")
        for i, task in enumerate(tasks, 1):
            st.write(f" {task}")
    else:
        st.write("まだ習慣化されるリストが登録されていません。リストを生成してください。")


    if st.button("習慣化リストを生成"):
        name = user_data.get("name")
        mbti = user_data.get("mbti")
        keystone_habits = user_data.get("habit_goal")
        prompt = (
            f"{name}さんは{mbti}の性格で、{keystone_habits}を習慣化したいと考えています。"
            f"この目標に基づいて、習慣化するのに最適な5つの具体的なタスクを提案してください。文章は優しいキャラクターが話しかけている口調にしてください。"
        )
        new_tasks = generate_tasks(prompt)

        try:
            task_ref.set({"tasks": new_tasks, "timestamp": firestore.SERVER_TIMESTAMP})
            st.success("新しいタスクが保存されました！")
        except Exception as e:
            st.error(f"タスクの保存中にエラーが発生しました: {e}")

    if task_data:
        st.subheader("今日やることをリストから選ぶ")
        selected_task = st.radio("リストの中から今日やりたいことを選択してね。さらに具体的な提案をしていくよ:", task_data.get("tasks", []))

        if selected_task:
            available_time = st.slider("今日使える時間は(分)どのくらい？:", 5, 120, 360)
            if st.button("今日やることの提案を生成"):
                prompt = (
                    f"タスク: {selected_task}"
                    f"{available_time}分で達成可能な、さらに具体的な提案をしてください。文章は優しいキャラクターが話しかけている口調にしてください。"
                )
                detailed_plan = generate_tasks(prompt)
                st.subheader("今日の具体的なプラン")
                for i, detail in enumerate(detailed_plan, 1):
                    st.write(f" {detail}")


    st.button("Done！", on_click=lambda: switch_page("成果"))