import streamlit as st
from PIL import Image
import base64
import random
from initializers import get_firestore_client
from datetime import date, datetime
import firebase_admin
from firebase_admin import credentials, initialize_app, firestore


def save_user_data(uid, mbti, habit_goal, name):
    try:
        db = get_firestore_client()
        user_ref = db.collection("users").document(uid)
        user_ref.set({"mbti": mbti, "habit_goal": habit_goal, "name": name})
        st.success("データが保存されました！")
    except Exception as e:
        st.error(f"データ保存中にエラーが発生しました: {e}")

def user_dashboard():
    try:
        db = get_firestore_client()
    except RuntimeError as e:
        st.error(f"Firestore クライアントの初期化エラー: {e}")
        return

    st.title("あなたのこと")
    st.text("")

    # 現在ログイン中のユーザーのUIDを取得
    if "user" in st.session_state and "uid" in st.session_state["user"]:
        uid = st.session_state["user"]["uid"]
    else:
        st.error("ログインしているユーザーが見つかりません。")
        return

    user_ref = db.collection("users").document(uid)
    user_data = user_ref.get().to_dict()

    if user_data and "mbti" in user_data and "habit_goal" in user_data and "name" in user_data:
        st.write("以下の情報がデータベースに保存されているよ:")
        container = st.container(border=True)
        container.write(f"**おなまえ**: {user_data.get('name', '未設定')}")
        container.write(f"**MBTI**: {user_data.get('mbti', '未設定')}")
        container.write(f"**習慣化したいこと**: {user_data.get('habit_goal', '未設定')}")

        st.divider()
        st.write("ここからあなたの情報を変更できるよ")

        # name（名前）の変更
        update_name = st.text_input("おなまえ")

        if st.button("おなまえの変更"):
            try:
                # Firestoreクライアントの初期化
                db = get_firestore_client()
            except RuntimeError as e:
                st.error(f"Firestore クライアントの初期化エラー: {e}")
                return

            # ログイン中のユーザーのUIDを取得
            uid = st.session_state.get("user", {}).get("uid")
            if not uid:
                st.error("ユーザー情報が取得できませんでした。ログイン状態を確認してください")
                return

            # Firestoreでの更新処理
            collection_name = "users"
            document_id = uid  # UIDを直接使用して対象のドキュメントを特定
            doc_ref = db.collection(collection_name).document(document_id)

            try:
                # ドキュメントが存在するか確認
                if not doc_ref.get().exists:
                    st.error(f"ユーザードキュメントが見つかりません (UID: {document_id})")
                    return

                # Firestoreを更新
                doc_ref.update({"name": update_name})
                st.success(f"おなまえを {update_name} に変更したよ")
            except Exception as e:
                st.error(f"Firestoreの更新中にエラーが発生しました: {e}")

        # MBTIの変更
        update_mbti = st.selectbox("MBTI",
            ["INFJ(提唱者)",
            "ISTJ(管理者)",
            "INFP(仲介者)",
            "INTJ(建築家)",
            "ISFJ(擁護者)",
            "ISFP(冒険家)",
            "INTP(論理学者)",
            "ESTJ(幹部)",
            "ESFJ(外交官)",
            "ESTP(起業家)",
            "ESFP(エンターテイナー)",
            "ENFJ(主人公)",
            "ENFP(活動家)",
            "ENTJ(指導者)",
            "ENTP(討論者)",
            "ISTP(巨匠)",])

        if st.button("MBTIの変更"):
            try:
                # Firestoreクライアントの初期化
                db = get_firestore_client()
            except RuntimeError as e:
                st.error(f"Firestore クライアントの初期化エラー: {e}")
                return

            # ログイン中のユーザーのUIDを取得
            uid = st.session_state.get("user", {}).get("uid")
            if not uid:
                st.error("ユーザー情報が取得できませんでした。ログイン状態を確認してください")
                return

            # Firestoreでの更新処理
            collection_name = "users"
            document_id = uid  # UIDを直接使用して対象のドキュメントを特定
            doc_ref = db.collection(collection_name).document(document_id)

            try:
                # ドキュメントが存在するか確認
                if not doc_ref.get().exists:
                    st.error(f"ユーザードキュメントが見つかりません (UID: {document_id})")
                    return

                # Firestoreを更新
                doc_ref.update({"mbti": update_mbti})
                st.success(f"MBTIを {update_mbti} に変更したよ")
            except Exception as e:
                st.error(f"Firestoreの更新中にエラーが発生しました: {e}")

        # habit_goal（習慣化したいこと）の変更
        update_habit = st.text_input("習慣化したいこと")

        if st.button("習慣化したいことの変更"):
            try:
                # Firestoreクライアントの初期化
                db = get_firestore_client()
            except RuntimeError as e:
                st.error(f"Firestore クライアントの初期化エラー: {e}")
                return

            # ログイン中のユーザーのUIDを取得
            uid = st.session_state.get("user", {}).get("uid")
            if not uid:
                st.error("ユーザー情報が取得できませんでした。ログイン状態を確認してください")
                return

            # Firestoreでの更新処理
            collection_name = "users"
            document_id = uid  # UIDを直接使用して対象のドキュメントを特定
            doc_ref = db.collection(collection_name).document(document_id)

            try:
                # ドキュメントが存在するか確認
                if not doc_ref.get().exists:
                    st.error(f"ユーザードキュメントが見つかりません (UID: {document_id})")
                    return

                # Firestoreを更新
                doc_ref.update({"habit_goal": update_habit})
                st.success(f"習慣化したいことを {update_habit} に変更したよ")
            except Exception as e:
                st.error(f"Firestoreの更新中にエラーが発生しました: {e}")

    else:
        st.write("やりたいのに続かないことってあるよね。")
        st.write("どーやったら続くか一緒に考えよ！まずは、あなたのことを教えて！")
        name = st.text_input("あなたのお名前を教えて")
        mbti = st.selectbox("あなたのMBTIを教えてね",
            ["INFJ(提唱者)",
            "ISTJ(管理者)",
            "INFP(仲介者)",
            "INTJ(建築家)",
            "ISFJ(擁護者)",
            "ISFP(冒険家)",
            "INTP(論理学者)",
            "ESTJ(幹部)",
            "ESFJ(外交官)",
            "ESTP(起業家)",
            "ESFP(エンターテイナー)",
            "ENFJ(主人公)",
            "ENFP(活動家)",
            "ENTJ(指導者)",
            "ENTP(討論者)",
            "ISTP(巨匠)",])
        habit_goal = st.text_input("習慣化したいことを教えてね")


        if st.button("保存"):
            save_user_data(uid, mbti, habit_goal,name)
            st.session_state["rerun"] = not st.session_state.get("rerun", False)

