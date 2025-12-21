import streamlit as st
import math
import statistics
import re

# --- ページ設定 ---
st.set_page_config(page_title="Scientific Calculator Pro", layout="centered")

st.markdown("""
<style>
    /* スクロール防止と全画面化 */
    html, body, [data-testid="stAppViewContainer"] {
        overflow: hidden !important;
        height: 100vh;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    .main .block-container { 
        padding: 0px !important; 
        max-width: 100% !important; 
        margin: 0px !important;
    }
    
    /* ボタンを横長にし、隙間を極限まで詰める */
    div.stButton > button {
        width: 100% !important; 
        height: 55px !important; /* 縦を少し抑えて横長感を強調 */
        font-size: 20px !important; 
        font-weight: 800 !important;
        margin: 0px !important; 
        padding: 0px !important;
        border: 1px solid #444 !important;
        border-radius: 0px !important;
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* ＝とDELETEボタン（さらに横長） */
    .wide-btn div.stButton > button { 
        height: 65px !important; 
        font-size: 26px !important; 
        background-color: #e0e0e0 !important; 
    }

    /* タイトルのスタイル */
    .calc-title {
        text-align: center;
        font-size: 20px;
        font-weight: bold;
        padding: 8px 0px;
        background-color: #1a1a1a;
        color: #ffffff;
        width: 100%;
    }

    /* カラム間の隙間をゼロにする */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }

    .display-box { 
        font-size: 40px; font-weight: bold; text-align: right; 
        padding: 15px; background: #000000; color: #00ff00; 
        border-bottom: 2px solid #333; min-height: 90px;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

# タイトルを表示
st.markdown('<div class="calc-title">SCIENTIFIC CALCULATOR PRO</div>', unsafe_allow_html=True)

if 'formula' not in st.session_state: st.session_state.formula = ""
if 'mode' not in st.session_state: st.session_state.mode = "通常"

# ディスプレイ
st.markdown(f'<div class="display-box">{st.session_state.formula if st.session_state.formula else "0"}</div>', unsafe_allow_html=True)

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
            u_map = {'Y':'1e24','M':'1e6','k':'1e3','m':'1e-3','n':'1e-9','p':'1e-12'}
            for sym, val in u_map.items(): f = re.sub(rf'(\d+){sym}', rf'(\1*{val})', f)
            res = eval(f, {"__builtins__": None}, {"math": math, "statistics": statistics})
            st.session_state.formula = format(res, '.10g')
        except: st.session_state.formula = "Error"
    elif char == "C": st.session_state.formula = ""
    elif char == "del": st.session_state.formula = current[:-1]
    else:
        ops = ["+", "×", "÷", "^^"]
        if not current and char in ops: return
        if current and current[-1] in (ops + ["−", "."]) and char in (ops + ["−", "."]): return
        st.session_state.formula += str(char)

def draw_row(labels, is_mode=False):
    cols = st.columns(len(labels))
    for i, l in enumerate(labels):
        if is_mode:
            if cols[i].button(l, key=f"m_{l}"):
                st.session_state.mode = l
                st.rerun()
        else:
            if cols[i].button(l, key=f"b_{l}_{i}_{st.session_state.mode}"):
                on_click(l)
                st.rerun()

# --- レイアウト（＋を一番上に配置） ---
draw_row(["+", "÷", "×", "−"]) # 演算子を一番上の行に集約
draw_row(["7", "8", "9", "C"])
draw_row(["4", "5", "6", "del"])
draw_row(["1", "2", "3", "0"])
draw_row([".", "00", "(", ")"])

st.markdown('<div class="wide-btn">', unsafe_allow_html=True)
c1, c2 = st.columns(2)
if c1.button("＝", key="eq"): on_click("＝"); st.rerun()
if c2.button("CLEAR ALL", key="ca"): st.session_state.formula = ""; st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# モード切替
draw_row(["通常", "科学計算", "巨数", "値数"], is_mode=True)

# モード別ボタン
if st.session_state.mode == "科学計算":
    draw_row(["sin(", "cos(", "tan(", "log("])
    draw_row(["abs(", "√", "exp", "π"])
elif st.session_state.mode == "巨数":
    draw_row(["n", "μ", "m", "k"])
    draw_row(["M", "G", "T", "P"])
elif st.session_state.mode == "値数":
    draw_row(["平均(", "中央値(", "max(", "min("])
