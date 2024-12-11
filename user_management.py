from firebase_admin import auth
import streamlit as st

def register_user(email, password):
    try:
        user = auth.create_user(email=email, password=password)
        st.success(f"新しいユーザーが作成されました: {user.uid}")
        return user
    except Exception as e:
        st.error(f"ユーザー登録中にエラーが発生しました: {e}")

def login_user(email):
    try:
        user = auth.get_user_by_email(email)
        st.session_state["user"] = {"email": user.email, "uid": user.uid}
        st.success(f"ようこそ、{email} さん！")
        return True
    except Exception as e:
        st.error(f"ログイン中にエラーが発生しました: {e}")
        return False
