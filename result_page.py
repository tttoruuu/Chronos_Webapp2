import streamlit as st
from PIL import Image

def switch_page(page_name):
    st.session_state["current_page"] = page_name

def result_page():
    st.title('クロノクエスト')
    st.text('')

    # 初期化: ページが読み込まれたときに1回だけ実行される
    if "progress" not in st.session_state:
        st.session_state.progress = 3  # 初期値を3%に設定

    days = "1"
    st.title(f"{days}日目")

    # プログレスバーの表示
    progress_text = ""
    my_bar = st.progress(st.session_state.progress, text=progress_text)

    # Rerunボタン
    #if st.button("Rerun"):
    #    st.session_state.progress = 3  # ボタンが押されたら進捗をリセット
    #    st.experimental_rerun()

    st.text('')

    #画像
    image = Image.open('ゆきだまちゃん.png')
    st.image(image, width=300)

    st.text('お疲れ様！えらい！えらすぎる！')
    st.text('短い時間なのに全力で頑張るなんて、本当に素敵！')
    st.text('ちゃんと休憩も忘れないでね。次も一緒にがんばろう！')
    st.text('')

    with st.form("my_form"):
        st.text('今日のタスクはどうだった？')

        st.text('難易度')
        # 3つのカラムを作成
        col1, col2, col3 = st.columns(3)

        # 各カラムにボタンを配置
        with col1:
            button1 = st.form_submit_button("簡単")
        with col2:
            button2 = st.form_submit_button("ふつう")
        with col3:
            button3 = st.form_submit_button("難しい")

        st.text('楽しさ')
        # 3つのカラムを作成
        col1, col2, col3 = st.columns(3)

        # 各カラムにボタンを配置
        with col1:
            button1 = st.form_submit_button("とても楽しい")
        with col2:
            button2 = st.form_submit_button("ふつうに楽しい")
        with col3:
            button3 = st.form_submit_button("楽しくない")

        st.form_submit_button("送信")


    st.button("戻る", on_click=lambda: switch_page("トレーニング"))

