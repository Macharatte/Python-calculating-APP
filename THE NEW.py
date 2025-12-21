import streamlit as st
import math
import statistics
import re

# --- ページ設定 ---
st.set_page_config(page_title="Python Calculator", layout="centered")

# --- カスタムデザインCSS ---
st.markdown("""
<style>
    header {visibility: hidden;}
    .main .block-container { padding-top: 2rem; max-width: 500px; }
    
    /* タイトル */
    .calc-title { text-align: center; font-size: 32px; font-weight: bold; margin-bottom: 20px; font-family: sans-serif; }
    
    /* ディスプレイ（入力欄） */
    .stTextInput input {
        font-size: 30px !important; height: 60px !important; text-align: right !important;
        background-color: #f8f9fa !important; border: 1px solid #ced4da !important;
    }

    /* 基本ボタン */
    div.stButton > button {
        width: 100% !important; height: 50px !important;
        font-size: 18px !important; border-radius: 8px !important;
        border: 1px solid #ccc !important; background-color: #fff !important; color: #333 !important;
    }

    /* 緑色の＝ボタン */
    .equal-btn div.stButton > button {
        background-color: #5cb85c !important; color: white !important; border: none !important;
        height: 60px !important; font-size: 24px !important;
    }

    /* オレンジ色のM+ボタン */
    .mem-btn div.stButton > button {
        background-color: #f0ad4e !important; color: white !important; border: none !important;
    }

    /* 水色のモードボタン */
    .mode-btn div.stButton > button {
        background-color: #add8e6 !important; color: #333 !important; border: none !important;
        height: 40px !important; font-size: 14px !important;
    }

    [data-testid="column"] { padding: 3px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="calc-title">python calculator</div>', unsafe_allow_html=True)

if 'formula' not in st.session_state: st.session_state.formula = ""
if 'mode' not in st.session_state: st.session_state.mode = "Normal"

# ディスプレイ
st.text_input("", value=st.session_state.formula if st.session_state.formula else "0", key="display", disabled=True)

def on_click(char):
    if st.session_state.formula == "Error": st.session_state.formula = ""
    
    if char == "=":
        try:
            f = st.session_state.formula.replace('×', '*').replace('÷', '/').replace('−', '-')
            # 数学的置換
            f = f.replace('^', '**').replace('π', 'math.pi').replace('e', 'math.e')
            res = eval(f, {"__builtins__": None}, {"math": math, "statistics": statistics})
            st.session_state.formula = format(res, '.10g')
        except: st.session_state.formula = "Error"
    elif char == "C": st.session_state.formula = ""
    elif char == "del": st.session_state.formula = st.session_state.formula[:-1]
    else: st.session_state.formula += str(char)

def draw_row(labels, css_class=""):
    cols = st.columns(len(labels))
    for i, l in enumerate(labels):
        with cols[i]:
            if st.button(l, key=f"btn_{l}_{i}_{st.session_state.mode}"):
                on_click(l); st.rerun()

# --- 6列ボタン配置 ---
draw_row(["sin", "cos", "tan", "e", "log", "π"])
draw_row(["abs", "round", "min", "max", "(", "e"]) # デザイン画像に基づく
draw_row(["4", "5", "6", "3", ")", "^"])
draw_row(["()", "000", "0", "C", "del", "i"])

# --- 特殊ボタン（＝, M+） ---
st.markdown('<div class="equal-btn">', unsafe_allow_html=True)
if st.button("＝", key="eq_main"): on_click("="); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="mem-btn">', unsafe_allow_html=True)
if st.button("M+", key="mem_add"): pass # メモリ機能が必要な場合はここに追加
st.markdown('</div>', unsafe_allow_html=True)

st.write("")

# --- モードボタン ---
st.markdown('<div class="mode-btn">', unsafe_allow_html=True)
m_cols = st.columns(4)
modes = ["Normal", "Sci", "Big", "Val"]
for i, m in enumerate(modes):
    if m_cols[i].button(m, key=f"mode_{m}"):
        st.session_state.mode = m
        st.rerun()
st.markdown('</div>', unsafe_allow_html=True)
