import os
import openai
from firebase_admin import credentials, initialize_app, firestore
import firebase_admin
import streamlit as st


def initialize_firebase(environment="production"):
    """Firebase アプリを初期化します。初期化済みの場合はスキップします。"""
    if not firebase_admin._apps:  # 初期化済みかチェック
        if environment == "local":
            # ローカル環境の設定
            firebase_key_path = os.getenv("FIREBASE_LOCAL_KEY")
            if firebase_key_path and os.path.exists(firebase_key_path):
                cred = credentials.Certificate(firebase_key_path)
                initialize_app(cred)
                
            else:
                raise FileNotFoundError(
                    f"Firebaseキーが見つかりません。指定されたパス: {firebase_key_path}"
                )
        else:
            # デプロイ環境の設定
            if "firebase" in st.secrets:
                firebase_secrets = dict(st.secrets["firebase"])
                cred = credentials.Certificate(firebase_secrets)
                initialize_app(cred)
         
            else:
                raise FileNotFoundError("Firebase 設定が secrets.toml に設定されていません。")
    else:
        st.write("")  # 再初期化をスキップ

#Firestoreの初期化（認証・設定）
def get_firestore_client():
    """Firestore クライアントを取得します。"""
    if not firebase_admin._apps:
        raise RuntimeError("Firebase が初期化されていません。")
    return firestore.client()


def initialize_openai(environment="production"):
    """OpenAI API を初期化します。"""
    if environment == "local":
        # ローカル環境の設定
        openai.api_key = os.getenv("OPENAI_API_KEY")
        if not openai.api_key:
            raise FileNotFoundError("OpenAI APIキーが .env に設定されていません。")
       
    else:
        # デプロイ環境の設定
        if "openai" in st.secrets:
            openai.api_key = st.secrets["openai"]["OPENAI_API_KEY"]
           
        else:
            raise FileNotFoundError("OpenAI APIキーが secrets.toml に設定されていません。")
