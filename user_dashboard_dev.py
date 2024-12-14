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

def user_dashboard_dev():
    try:
        db = get_firestore_client()
    except RuntimeError as e:
        st.error(f"Firestore クライアントの初期化エラー: {e}")
        return

    #画像
    image = Image.open('GOD.png')
    st.image(image, width=600)

    st.title("時の部屋")
    st.subheader("開発者専用画面です。")

    # 現在ログイン中のユーザーのUIDを取得
    if "user" in st.session_state and "uid" in st.session_state["user"]:
        uid = st.session_state["user"]["uid"]
    else:
        st.error("ログインしているユーザーが見つかりません。")
        return

    st.write(f"現在のUID: {st.session_state['user']['uid']}")

    user_ref = db.collection("users").document(uid)
    user_data = user_ref.get().to_dict()

    st.text("")

    if user_data:
        name = user_data.get('name')
        st.write(f"クロノス神「＜{name}＞については、以下の情報がデータベースに保存されておる」")
        container = st.container(border=True)
        container.write(f"**last_done_date**: {user_data.get('last_done_date', '未設定')}")
        container.write(f"**done_count**: {user_data.get('done_count', '未設定')}")
        container.write(f"**last_login_date**: {user_data.get('last_login_date', '未設定')}")

        st.divider()
        st.write("クロノス神「そなたに、時を操る力を授けよう。望みのままに入力し変更するがよい」")
        #last_done_date（最新DONE日）の変更
        update_done_date = st.date_input("last_done_date更新")

        if st.button("last_done_dateの変更"):
            # 入力値の検証
            if not update_done_date:
                st.error("日付を入力してください")
                return

            try:
                # 日付を文字列に変換 (st.date_inputはdatetime.date型を返す)
                update_done_date_str = update_done_date.strftime("%Y-%m-%d")
            except AttributeError:
                st.error("日付入力に問題があります。再度確認してください")
                return

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

                # Firestoreに日付を更新
                doc_ref.update({"last_done_date": update_done_date_str})
                st.success(f"クロノス神「ふむ。last_done_dateを {update_done_date_str} に変更したのじゃな」")
            except Exception as e:
                st.error(f"Firestoreの更新中にエラーが発生しました: {e}")

        #done_count（Done日数）の変更
        default_count = user_data.get('done_count')
        update_done_co = st.number_input("done_count更新", min_value=0, value=default_count, step=1)
        if st.button("done_countの変更"):
            # 入力チェック: 空入力の場合
            if not update_done_co:
                st.error("更新するDone回数を入力してください")
                return

            try:
                # 入力値を整数に変換
                done_count = int(update_done_co)
            except ValueError:
                st.error("Done回数には整数を入力してください")
                return

            # Firestoreクライアントの初期化
            try:
                db = get_firestore_client()
            except RuntimeError as e:
                st.error(f"Firestore クライアントの初期化エラー: {e}")
                return

            # ログイン中のユーザーのUIDを取得
            uid = st.session_state["user"]["uid"]

            # 更新対象のコレクションとドキュメントID
            collection_name = "users"
            document_id = uid  # UIDを直接使用して対象のドキュメントを特定

            # ドキュメント参照を取得
            doc_ref = db.collection(collection_name).document(document_id)

            # ドキュメントが存在するか確認
            if not doc_ref.get().exists:
                st.error(f"ユーザードキュメントが見つかりません (UID: {document_id})")
                return

            # Firestoreでの更新処理
            try:
                doc_ref.update({"done_count": done_count})  # フィールドを更新
                st.success(f"クロノス神「なんと！　Done回数を {done_count}回に変更するとは・・」")
            except Exception as e:
                st.error(f"Firestoreの更新中にエラーが発生しました: {e}")

        #last_login_date（最新ログイン日）の変更
        update_login_date = st.date_input("last_login_date更新")

        if st.button("last_login_dateの変更"):
            # 入力値の検証
            if not update_login_date:
                st.error("日付を入力してください")
                return

            try:
                # 日付を文字列に変換 (st.date_inputはdatetime.date型を返す)
                update_login_date_str = update_login_date.strftime("%Y-%m-%d")
            except AttributeError:
                st.error("日付入力に問題があります。再度確認してください")
                return

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

                # Firestoreに日付を更新
                doc_ref.update({"last_login_date": update_login_date_str})
                st.success(f"クロノス神「ほっほっほっ。last_login_dateを {update_login_date_str} に変更するとは、愉快じゃのうw」")
            except Exception as e:
                st.error(f"Firestoreの更新中にエラーが発生しました: {e}")


    else:
        st.error("ユーザー情報がデータベースに存在しません。")
