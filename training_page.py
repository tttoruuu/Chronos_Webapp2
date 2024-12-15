import streamlit as st
from openai import OpenAI
import openai
import os
from initializers import get_firestore_client
from google.cloud import firestore
import re
from datetime import date, datetime
import firebase_admin
from firebase_admin import credentials, initialize_app, firestore

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
    
    ### 20241214 3:00 しょうさん追加
    today = date.today()
    last_done = user_data.get("last_done_date")

    if last_done is None:
        st.text("はじめまして！わたしはゆきだま！あなたのがんばりたいことを応援するよ！") 
    else:
        last_done = datetime.strptime(last_done, "%Y-%m-%d").date() 
        done_days_gap = (today - last_done).days

        if done_days_gap == 0:
            st.text(f"今日のタスクは完了してるよ！もうちょっとがんばってみる？") 
        elif done_days_gap == 1:
            st.text(f"毎日がんばってるね！とってもステキだよ！") 
        elif done_days_gap >= 5:
            st.text(f"前回のタスク完了から{done_days_gap}日ぶりだね。ゆきだま、会えなくてちょっと寂しかったな・・") 
        else:
            st.text(f"前回のタスク完了から{done_days_gap}日ぶりだね。会えてうれしいよ！") 
    
    # Firestore のデータを取得して表示
    name = user_data.get("name")
    mbti = user_data.get("mbti")
    keystone_habits = user_data.get("habit_goal")

    # セッション状態の初期化
    if 'form_submitted' not in st.session_state:
        st.session_state['form_submitted'] = False
    if 'done_clicked' not in st.session_state:
        st.session_state['done_clicked'] = False
    ###

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


        # 20241214 22:44だま修正
        if selected_task:
            available_time = st.selectbox(
                "今日使える時間はどのくらい？:", 
                ["5分", "15分", "30分", "1時間", "2-3時間", "4-5時間","6時間以上"]
                )
            generate_btn = st.button("今日やることの提案を生成")
            if generate_btn:
                st.session_state['form_submitted'] = True
        
            if st.session_state['form_submitted']:
                prompt = (
                    f"タスク: {selected_task}"
                    f"{available_time}で達成可能な、さらに具体的な提案をしてください。文章は優しいキャラクターが話しかけている口調にしてください。"
                )
                detailed_plan = generate_tasks(prompt)
                st.subheader("今日の具体的なプラン")
                for i, detail in enumerate(detailed_plan, 1):
                    st.write(f" {detail}")

                if st.button("DONE!", key="done_button", icon="🔥", use_container_width=True):
                    st.session_state['done_clicked'] = True
                    try:
                        uid = st.session_state["user"]["uid"]
                        user_ref = db.collection("users").document(uid)
                        user_data = user_ref.get().to_dict()

                        today = date.today()
                        last_done = user_data.get("last_done_date") if user_data else None
                        done_co = user_data.get("done_count", 0) if user_data else 0

                        if last_done is not None:
                            last_done = datetime.strptime(last_done, "%Y-%m-%d").date()
                            done_days_gap = (today - last_done).days
                            if done_days_gap > 0:
                                done_co += 1
                        else:
                            done_co = 1

                        today_str = today.strftime("%Y-%m-%d")

                        # Firestoreの更新をより明示的に
                        user_ref.update({
                            "done_count": done_co,
                            "last_done_date": today_str
                        })
                        
                        st.session_state['done_message'] = f"Done回数を {done_co}回に、 最新Done日を {today_str} に更新したよ！" 
                    
                    except Exception as e:
                        st.error(f"Firestoreの更新中にエラーが発生しました: {e}")

            # メッセージの表示
            if 'done_message' in st.session_state and st.session_state['done_clicked']:
                st.success(st.session_state['done_message'])
                
                # リセットボタン
                if st.button("リセット", key="reset_button", use_container_width=True):
                    # セッション状態をリセット
                    st.session_state['done_message'] = None
                    st.session_state['done_clicked'] = False
                    st.session_state['form_submitted'] = False
                    st.rerun()  # ページを再読み込みして状態をリセット
