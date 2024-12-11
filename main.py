import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
from firebase import initialize_firebase
from user_management import register_user, login_user
from user_dashboard import user_dashboard
from firebase import db
from training_page import training_page
from result_page import result_page
from login_page import login_page

#ローカル環境で動くためのコード
if os.path.exists(".env"):
    from user_dashboard import user_dashboard
    load_dotenv()


#ここでfirebaseの環境設定
if "firebase_initialized" not in st.session_state:
    initialize_firebase()
    st.session_state["firebase_initialized"] = True

# Firebase の初期化を最初に実行
db = initialize_firebase()

def app():
    # サイドバーでページを選択
    st.sidebar.title("ナビゲーション")
    page = st.sidebar.radio("ページを選択してください", ["ログイン", "ユーザー情報入力", "トレーニング", "成果"])

     # セッション状態に基づいてページを表示
    if "page" not in st.session_state:
        st.session_state["page"] = "ログイン"

    if page == "ログイン":
        login_page()
    elif page == "ユーザー情報入力":
        user_dashboard()
    elif page == "トレーニング":
        training_page()
    elif page == "成果":
        result_page()
    

    # ゆきだまちゃんの表示
    image = Image.open("ゆきだまちゃん.png")
    st.image(image, width=300)

 

    #ログイン成功の場合に左端に「ログイン中」→ユーザー設定画面
    if "user" in st.session_state:
        st.sidebar.success(f"ログイン中: {st.session_state['user']['email']}")
        return


if __name__ == "__main__":
    app()
