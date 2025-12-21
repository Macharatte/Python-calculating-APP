import streamlit as st
import math
import statistics
import re

# --- ページ設定（スクロール防止と全画面化） ---
st.set_page_config(page_title="Calculator Pro", layout="centered")

st.markdown("""
<style>
    /* 全体のスクロールを禁止 */
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        height: 100vh;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* 画面の余白を完全排除 */
    .main .block-container { 
        padding: 0px !important; 
        max-width: 100% !important; 
        margin: 0px !important;
    }
    
    /* ボタンを横長に敷き詰める設定 */
    div.stButton > button {
        width: 100% !important; 
        height: 60px !important; 
        font-size: 24px !important; 
        font-weight: 800 !important;
        margin: 0px !important; 
        padding: 0px !important;
        border: 1px solid #000 !important;
        border-radius: 0px !important;
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* ＝とDELETEボタン（さらに強調） */
    .wide-btn div.stButton > button { 
        height: 75px !important; 
        font-size: 30px !important; 
        background-color: #e0e0e0 !important; 
    }

    /* モードボタン */
    .mode-btn div.stButton > button {
        height: 45px !important;
        font-size: 16px !important;
        background-color: #333 !important;
        color: #fff !important;
    }

    /* カラム間の隙間をゼロにする魔法の指定 */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; flex: 1 1 0% !important; min-width: 0px !important; }
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }

    /* ディスプレイ表示 */
    .display-box { 
        font-size: 45px; font-weight: bold; text-align: right; 
        padding: 20px; background: #000000; color: #00ff00; 
        border-bottom: 2px solid #333; min-height: 100px;
        font-family: monospace;
    }
    
    /* タイトル表示 */
    .calc-title {
        text-align: center; font-size: 20px; font-weight: bold;
        padding: 10px; background: #1a1a1a; color: white;
    }
</style>
""", unsafe_allow_html=True)

# タイトルの復活
st.markdown('<div class="calc-title">SCIENTIFIC CALCULATOR PRO</div>', unsafe_allow_html=True)

if 'formula' not in st.session_state: st.session_state.formula = ""
if 'mode' not in st.session_state: st.session_state.mode = "通常"

# ディスプレイ表示
st.markdown(f'<div class="display-box">{st.session_state.formula if st.session_state.formula else "0"}</div>', unsafe_allow_html=True)

# --- 共通入力ロジック ---
def on_click(char):
    current = st.session_state.formula
    if current == "Error":
        st.session_state.formula = ""
        if char in ["＝", "C", "del"]: return
        current = ""

    if char == "＝":
        if not current: return
        try:
            f = current.replace('×', '*').replace('÷', '/').replace('−', '-')
            f = f.replace('√', 'math.sqrt').replace('^^', '**').replace('π', 'math.pi')
            u_map
