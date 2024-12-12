import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import openai
from firebase_admin import credentials, initialize_app
import firebase_admin
from initializers import initialize_firebase, initialize_openai
from user_management import register_user, login_user
from user_dashboard import user_dashboard
from training_page import training_page
from result_page import result_page
from login_page import login_page


# 環境変数をロード（ローカル環境用）
if os.path.exists(".env"):
    load_dotenv()

# 環境の判別
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")  # デフォルトは "production"

def app():
    """アプリケーションのメインロジック"""
    # 初期化
    initialize_firebase(environment=ENVIRONMENT)
    st.write("Firestore クライアントが初期化されました。")
    initialize_openai(environment=ENVIRONMENT)

    # サイドバーでページを選択
    st.sidebar.title("ナビゲーション")
    page = st.sidebar.radio("ページを選択してください", ["ログイン", "ユーザー情報入力", "トレーニング", "成果"])

    # ページの表示
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

    # ログイン成功の場合に左端に「ログイン中」→ユーザー設定画面
    if "user" in st.session_state:
        st.sidebar.success(f"ログイン中: {st.session_state['user']['email']}")


if __name__ == "__main__":
    app()
