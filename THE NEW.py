import streamlit as st
import math
import statistics
import re

# --- ページ設定（スクロール防止と全画面化） ---
st.set_page_config(page_title="Calculator Pro", layout="centered")

st.markdown("""
<style>
    /* スクロールを禁止し、画面内に収める */
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
    
    /* ボタンの高さを1画面に収まるよう調整 (80px -> 60px前後) */
    div.stButton > button {
        width: 100% !important; 
        height: 60px !important; 
        font-size: 22px !important; 
        font-weight: 800 !important;
        margin: 0px !important; 
        border: 1px solid #000 !important;
        border-radius: 0px !important;
        background-color: #ffffff !important;
        color: #000000 !important;
    }

    /* ＝とDELETEボタンの高さ */
    .wide-btn div.stButton > button { 
        height: 75px !important; 
        font-size: 28px !important; 
        background-color: #f0f0f0 !important; 
    }

    /* モードボタン専用スタイル */
    .mode-btn div.stButton > button {
        height: 45px !important;
        font-size: 16px !important;
        background-color: #333 !important;
        color: #fff !important;
    }

    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }

    .display-box { 
        font-size: 42px; font-weight: bold; text-align: right; 
        padding: 20px; background: #000000; color: #00ff00; 
        border-bottom: 3px solid #333; min-height: 100px;
        font-family: monospace;
    }
</style>
""", unsafe_allow_html=True)

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
            u_map = {'Y':'1e24','M':'1e6','k':'1e3','m':'1e-3','n':'1e-9','p':'1e-12','f':'1e-15','a':'1e-18'}
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
        # モード切替と通常の入力を分離
        if is_mode:
            if cols[i].button(l, key=f"m_{l}"):
                st.session_state.mode = l
                st.rerun()
        else:
            if cols[i].button(l, key=f"b_{l}_{i}_{st.session_state.mode}"):
                on_click(l)
                st.rerun()

# --- メインレイアウト（4段＋操作2段＋モード＋機能） ---
draw_row(["7", "8", "9", "÷"])
draw_row(["4", "5", "6", "×"])
draw_row(["1", "2", "3", "−"])
draw_row(["0", ".", "C", "+"])

st.markdown('<div class="wide-btn">', unsafe_allow_html=True)
c1, c2 = st.columns(2)
if c1.button("＝", key="eq"): on_click("＝"); st.rerun()
if c2.button("DEL", key="dl"): on_click("del"); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# モード切替セクション
st.markdown('<div class="mode-btn">', unsafe_allow_html=True)
draw_row(["通常", "科学計算", "巨数", "値数"], is_mode=True)
st.markdown('</div>', unsafe_allow_html=True)

# モード別ボタン表示（ここも1画面に収まるよう2段まで）
if st.session_state.mode == "通常":
    draw_row(["(", ")", "00", "π"])
elif st.session_state.mode == "科学計算":
    draw_row(["sin(", "cos(", "tan(", "log("])
    draw_row(["abs(", "√", "exp", "^^"])
elif st.session_state.mode == "巨数":
    draw_row(["n", "μ", "m", "k"])
    draw_row(["M", "G", "T", "P"])
elif st.session_state.mode == "値数":
    draw_row(["平均(", "中央値(", "max(", "min("])
