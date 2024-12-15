import os
import streamlit as st
from PIL import Image
from dotenv import load_dotenv
import openai
import firebase_admin
from firebase_admin import credentials, initialize_app, firestore
from initializers import initialize_firebase, initialize_openai
from user_management import register_user, login_user
from user_dashboard import user_dashboard
from user_dashboard_dev import user_dashboard_dev
from training_page import training_page
from result_page import result_page
from login_page import login_page

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Aoboshi+One&display=swap');

    /* サイドバータイトル用のスタイル */
    .sidebar-title {
        font-family: 'Aoboshi One', serif;  /* フォントを Aoboshi One に変更 */
        font-size: 26px;  /* フォントサイズを調整 */
        color: #333333;   /* 色を調整 */
        text-align: center; /* 中央揃え */
        margin-bottom: 20px; /* 下にスペースを追加 */
    }
    </style>
    """,
    unsafe_allow_html=True
)


# 環境変数をロード（ローカル環境用）
if os.path.exists(".env"):
    load_dotenv()

# 環境の判別
ENVIRONMENT = os.getenv("ENVIRONMENT", "production")  # デフォルトは "production"

def app():
    """アプリケーションのメインロジック"""
    initialize_firebase(environment=ENVIRONMENT)
    st.write("Firebase 初期化完了")
    initialize_openai(environment=ENVIRONMENT)

    # サイドバーでタイトルを表示（HTML）
    st.sidebar.markdown('<div class="sidebar-title">クロノクエスト</div>', unsafe_allow_html=True)

    # サイドバーでページを選択
    st.sidebar.header("ナビゲーション")
    page = st.sidebar.radio("ページを選択してください", ["ログイン", "ユーザー情報入力", "今日のやること", "成果", "Dev専用_時の部屋"])

    # ページの表示
    if page == "ログイン":
        login_page()
    elif page == "ユーザー情報入力":
        user_dashboard()
    elif page == "今日のやること":
        training_page()
    elif page == "成果":
        result_page()
    elif page == "Dev専用_時の部屋":
        user_dashboard_dev()
    
    # サイドバーにゆきだまちゃんを表示
    st.sidebar.image(
        "ゆきだまちゃん.png",  # ローカルの画像パスまたはURL
        caption="ゆきだまちゃん",
        use_container_width=True  # サイドバー幅に合わせる
    )

    st.sidebar.write("私は雪の妖精！あなたのやりたいことを応援するね！")

    # ログイン成功の場合に左端に「ログイン中」→ユーザー設定画面
    if "user" in st.session_state:
        st.sidebar.success(f"ログイン中: {st.session_state['user']['email']}")


if __name__ == "__main__":
    app()
