import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from langchain_openai import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
import streamlit as st

# APIキーの確認
if not OPENAI_API_KEY:
    st.error("OPENAI_API_KEYが設定されていません。.envファイルを確認してください。")
    st.stop()

# LLMの初期化（APIキー確認後）
try:
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        # model="gpt-3.5-turbo",  # より安定したモデル
        temperature=0,
        openai_api_key=OPENAI_API_KEY
        # api_key=OPENAI_API_KEY        
    )
    st.sidebar.success("✅ LLM初期化成功") 
except Exception as e:
    st.error(f"LLMの初期化に失敗しました: {e}")
    st.stop()

st.title("【提出課題】LLM機能を搭載したWebアプリを開発しよう")

st.write("##### 専門家A: 年金の専門家")
st.write("入力フォームにテキストを入力し、「実行」ボタンを押すことで年金に関する相談ができます。")
st.write("##### 専門家B: 株式投資の専門家")
st.write("入力フォームにテキストを入力し、「実行」ボタンを押すことで株式投資に関する相談ができます。")

selected_item = st.radio(
    "動作モードを選択してください。",
    ["年金の相談", "株式投資の相談"]
)

st.divider()

# 入力フィールド
if selected_item == "年金の相談":
    input_message = st.text_input(label="年金の相談を入力してください。")
else:
    input_message = st.text_input(label="株式投資の相談を入力してください。")

# 実行ボタンが押された時のみLLMを呼び出し
if st.button("実行"):
    if input_message:
        st.divider()
        
        # メッセージの準備
        if selected_item == "年金の相談":
            st.write("年金の専門家に相談します。")
            messages = [
                SystemMessage(content="あなたは年金の専門家です。ユーザーの質問に対して、正確で分かりやすい回答を提供してください。"),
                HumanMessage(content=input_message),
            ]
        else:
            st.write("株式投資の専門家に相談します。")
            messages = [
                SystemMessage(content="あなたは株式投資の専門家です。ユーザーの質問に対して、正確で分かりやすい回答を提供してください。"),
                HumanMessage(content=input_message),
            ]
        
        st.write(f"入力内容: {input_message}")
        st.write("以下の回答を表示します。")
        
        # LLMの実行（エラーハンドリング付き）
        try:
            with st.spinner("回答を生成中..."):
                result = llm.invoke(messages)  # 修正: invoke()メソッドを使用
                # result = llm.invoke({"messages": messages})
                st.success("回答が生成されました！")
                st.write("**回答:**")
                st.write(result.content)
        except Exception as e:
            st.error(f"エラーが発生しました: {e}")
            st.error("APIキーやネットワーク接続を確認してください。")
    else:
        st.error("テキストを入力してから「実行」ボタンを押してください。")

