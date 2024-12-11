import os
import streamlit as st
from firebase_admin import credentials, initialize_app, firestore
import firebase_admin

def initialize_firebase():
    if not firebase_admin._apps:
        # ローカルかデプロイか判別
        if os.getenv("ENV", "production") == "local":
            # ローカル環境
            firebase_key_path = os.getenv("FIREBASE_LOCAL_KEY")
            if firebase_key_path and os.path.exists(firebase_key_path):
                cred = credentials.Certificate(firebase_key_path)
            else:
                raise FileNotFoundError("ローカル環境のFirebaseキーが見つかりません。")
        else:
            # デプロイ環境（secrets.toml を使用）
            try:
                if "firebase" in st.secrets:
                    firebase_secrets = dict(st.secrets["firebase"])
                    cred = credentials.Certificate(firebase_secrets)
                else:
                    raise FileNotFoundError("デプロイ環境のFirebase秘密情報が見つかりません。")
            except FileNotFoundError:
                raise FileNotFoundError(
                    "No secrets.toml file found. Ensure secrets.toml is set up correctly."
                )
        initialize_app(cred)
    return firestore.client()

try:
    db = initialize_firebase()
except FileNotFoundError as e:
    st.error(f"Firebaseの初期化エラー: {e}")
    db = None
