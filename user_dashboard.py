import streamlit as st
from firebase import db

def save_user_data(uid, mbti, habit_goal,name):
    try:
        user_ref = db.collection("users").document(uid)
        user_ref.set({"mbti": mbti, "habit_goal": habit_goal, "name":name})
        st.success("データが保存されました！")
    except Exception as e:
        st.error(f"データ保存中にエラーが発生しました: {e}")

def user_dashboard():
    st.title("あなたのこと")

    uid = st.session_state["user"]["uid"]
    user_ref = db.collection("users").document(uid)
    user_data = user_ref.get().to_dict()

    if user_data and "mbti" in user_data and "habit_goal" in user_data and "name" in user_data:
        st.write("以下の情報がデータベースに保存されています:")
        st.write(f"**おなまえ**: {user_data['name']}")
        st.write(f"**MBTI**: {user_data['mbti']}")
        st.write(f"**習慣化したいこと**: {user_data['habit_goal']}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("これでOK"):
                st.success("次のページに進みます。")
                st.stop()


        with col2:
            if st.button("やり直す"):
                st.warning("既存のデータをキャンセルし、再入力します。")
                user_ref.delete()
                st.session_state["rerun"] = not st.session_state.get("rerun", False)
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
