from user_management import register_user, login_user
import streamlit as st

def login_page():
    mode = st.radio("選択してください", ["ログイン", "新規登録"])

    #新規登録
    if mode == "新規登録":
        st.subheader("新規登録")
        email = st.text_input("メールアドレス")
        password = st.text_input("パスワード", type="password")
        if st.button("登録"):
            user = register_user(email, password)
            if user:
                st.session_state["user"] = {"email": email, "uid": user.uid}
                st.session_state["rerun"] = not st.session_state.get("rerun", False)
    #ログイン
    elif mode == "ログイン":
        st.subheader("ログイン")
        email = st.text_input("メールアドレス")
        password = st.text_input("パスワード", type="password")
        if st.button("ログイン"):
            success = login_user(email)
            if success:
                st.session_state["page"] = "ユーザー情報入力"  # ログイン後に次のページへ遷移
