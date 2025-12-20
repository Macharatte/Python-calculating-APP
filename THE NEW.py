import streamlit as st
import math

# --- ページ設定 ---
st.set_page_config(page_title="Scientific Calculator")

# --- タイトル表示 ---
st.title("科学計算電卓")

# --- 計算状態の管理 ---
if 'formula' not in st.session_state:
    st.session_state.formula = ""

# --- 計算ロジック ---
def press(char):
    if char == "=":
        try:
            # 記号を計算可能な形に変換
            f = st.session_state.formula.replace('×', '*').replace('÷', '/')
            st.session_state.formula = str(eval(f))
        except:
            st.session_state.formula = "Error"
    elif char == "C":
        st.session_state.formula = ""
    else:
        st.session_state.formula += str(char)

# --- 画面表示 ---
st.text_input("入力された式", value=st.session_state.formula, key="display")

# --- ボタン配置 ---
col1, col2, col3, col4 = st.columns(4)
buttons = [
    '7', '8', '9', '÷',
    '4', '5', '6', '×',
    '1', '2', '3', '-',
    '0', '.', 'C', '='
]

for i, b in enumerate(buttons):
    cols = [col1, col2, col3, col4]
    if cols[i % 4].button(b):
        press(b)
        st.rerun()
