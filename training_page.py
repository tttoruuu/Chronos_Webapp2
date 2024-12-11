from firebase import db
import streamlit as st
from openai import OpenAI
import openai
import os

# Streamlit SecretsからAPIキーを取得
OpenAI.api_key = st.secrets["openai"]["OPENAI_API_KEY"]

def switch_page(page_name):
    st.session_state["current_page"] = page_name

def training_page():
    uid = st.session_state["user"]["uid"]
    user_ref = db.collection("users").document(uid)
    user_data = user_ref.get().to_dict()
    
    with st.form(key="mbti_form"):
        availabletime = str(st.slider("今日使える時間(分)", 5,120,360))    
        submit_btn = st.form_submit_button(label="登録")

    # Firestore のデータを取得して表示
    name = user_data.get("name")
    mbti = user_data.get("mbti")
    KeystoneHabits = user_data.get("habit_goal")
    
    #ボタンが押されたら
    if submit_btn:
        st.text(f"ようこそ！{name}さん！") 
        st.text(f"{name}さんのやりたいことを応援するね！")
        st.text("さっそく今日やることを決めよう")

        def run_gpt(name,mbti,KeystoneHabits,availabletime):
            request_to_gpt = name + " は、" + mbti + "な性格の人です。" + KeystoneHabits + "を習慣化して取り組みたいと考えています。" + mbti + "な性格の人が楽しんで取り組めるように応援しながら、" + str(availabletime) + "分でできるタスクを、タスクのタイトル、概要、詳細の順番で複数個出力してください。内容は300文字以内で出力してください。また、文章は優しいキャラクターが話しかけている口調にしてください。"

        # 決めた内容を元にclient.chat.completions.createでchatGPTにリクエスト。オプションとしてmodelにAIモデル、messagesに内容を指定
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": request_to_gpt },
                ],
            )
            # 返って来たレスポンスの内容はresponse.choices[0].message.content.strip()に格納されているので、これをoutput_contentに代入
            output_content = response.choices[0].message.content.strip()
            return output_content # 返って来たレスポンスの内容を返す

        output_content_text = run_gpt(name,mbti,KeystoneHabits,availabletime)
        st.write(output_content_text)

        st.button("Done！", on_click=lambda: switch_page("成果"))