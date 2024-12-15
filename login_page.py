from user_management import register_user, login_user
import streamlit as st
from datetime import date, datetime
from initializers import get_firestore_client
from pathlib import Path

# CSSファイルを読み込む関数
def load_css(file_name):
    css_path = Path(f"static/{file_name}")
    with open(css_path, "r", encoding="utf-8") as css_file:
        st.markdown(f"<style>{css_file.read()}</style>", unsafe_allow_html=True)

# CSSをロード
load_css("styles.css")

def login_page():
    st.markdown('<h1 class="custom-title">クロノスクエスト</h1>', unsafe_allow_html=True)
    st.write('このアプリは、習慣化の走り出しを応援するアプリです')
    st.write('ゆきだまちゃんと一緒に素敵な習慣を作ろう！')
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
                # login_date更新

                try:
                    db = get_firestore_client()
                except RuntimeError as e:
                    st.error(f"Firestore クライアントの初期化エラー: {e}")
                    return

                # ログイン中のユーザーのUIDを取得
                uid = st.session_state["user"]["uid"]

                # 今日の日付を取得
                today = date.today()  # 例: 2024-12-12
                today_str = today.strftime("%Y-%m-%d")

                # 更新対象のコレクションとドキュメントID
                collection_name = "users"
                document_id = uid  # UIDを直接使用して対象のドキュメントを特定

                # ドキュメント参照を取得
                doc_ref = db.collection(collection_name).document(document_id)

                # ドキュメントが存在するか確認
                if not doc_ref.get().exists:
                    st.error(f"ユーザードキュメントが見つかりません (UID: {document_id})")
                    return

                # フィールドを更新
                doc_ref.update({"last_login_date": today_str})

                st.write(f"最新ログイン日を {today} に更新完了！")

                st.session_state["page"] = "ユーザー情報入力"  # ログイン後に次のページへ遷移