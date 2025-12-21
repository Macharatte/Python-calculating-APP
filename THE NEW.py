import streamlit as st
import math
import statistics
import re

# --- ページ設定 ---
st.set_page_config(page_title="Python Calculator", layout="centered")

# --- 黒基調のデザインCSS ---
st.markdown("""
<style>
    header {visibility: hidden;}
    .main .block-container { padding-top: 2rem; max-width: 600px; }
    
    .calc-title { 
        text-align: center; font-size: 42px; font-weight: 800; 
        color: #000; margin-bottom: 20px; font-family: sans-serif; 
    }
    
    .display-container {
        display: flex; align-items: center; justify-content: flex-end;
        font-size: 55px; font-weight: bold; color: #000;
        margin-bottom: 20px; padding: 10px; border-bottom: 3px solid #000;
    }

    /* ボタンデザイン：黒背景・白文字 */
    div.stButton > button {
        width: 100% !important; height: 55px !important;
        font-size: 20px !important; border-radius: 8px !important;
        border: none !important; background-color: #000000 !important;
        color: #ffffff !important; font-weight: bold !important;
    }
    
    /* ＝ ボタン */
    .eq-container div.stButton > button { height: 55px !important; background-color: #333 !important; }

    /* delete ボタン */
    .delete-btn div.stButton > button {
        background-color: #FF0000 !important; color: white !important;
        height: 60px !important; font-size: 22px !important; margin-top: 10px !important;
    }

    /* モードボタン（選択中をわかりやすく） */
    .mode-btn div.stButton > button {
        height: 40px !important; font-size: 14px !important;
        background-color: #444 !important;
    }

    [data-testid="column"] { padding: 4px !important; }
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="calc-title">python calculator</div>', unsafe_allow_html=True)

if 'formula' not in st.session_state: st.session_state.formula = ""
if 'mode' not in st.session_state: st.session_state.mode = "通常"

st.markdown(f'<div class="display-container"><span>{st.session_state.formula if st.session_state.formula else "0"}</span></div>', unsafe_allow_html=True)

def on_click(char):
    current = st.session_state.formula
    if current == "Error":
        st.session_state.formula = ""
        if char in ["=", "delete"]: return
        current = ""
    if char == "=":
        if not current: return
        try:
            f = current.replace('×', '*').replace('÷', '/').replace('−', '-')
            f = f.replace('√', 'math.sqrt').replace('^^', '**').replace('π', 'math.pi').replace('e', 'math.e')
            # 単位変換マップ（ヨクトからヨタまで）
            u_map = {
                'Y': '1e24', 'Z': '1e21', 'E': '1e18', 'P': '1e15', 'T': '1e12', 'G': '1e9', 'M': '1e6', 'k': '1e3', 'h': '1e2', 'da': '1e1',
                'd': '1e-1', 'c': '1e-2', 'm': '1e-3', 'μ': '1e-6', 'n': '1e-9', 'p': '1e-12', 'f': '1e-15', 'a': '1e-18', 'z': '1e-21', 'y': '1e-24'
            }
            for sym, val in u_map.items(): f = re.sub(rf'(\d+){sym}', rf'(\1*{val})', f)
            res = eval(f, {"__builtins__": None}, {"math": math, "statistics": statistics})
            st.session_state.formula = format(res, '.10g')
        except: st.session_state.formula = "Error"
    elif char == "delete": st.session_state.formula = ""
    else: st.session_state.formula += str(char)

def draw_row(labels):
    cols = st.columns(len(labels))
    for i, l in enumerate(labels):
        if cols[i].button(l, key=f"btn_{l}_{i}_{st.session_state.mode}"):
            on_click(l); st.rerun()

# メインボタン
draw_row(["7", "8", "9", "π", "÷", "+"])
draw_row(["4", "5", "6", "e", "√", "−"])
draw_row(["1", "2", "3", "i", "^^", "×"])

c1, c2, c3, c4 = st.columns([1, 1, 1, 3])
with c1: 
    if st.button("()"): on_click("()"); st.rerun()
with c2: 
    if st.button("0"): on_click("0"); st.rerun()
with c3: 
    if st.button("."): on_click("."); st.rerun()
with c4:
    st.markdown('<div class="eq-container">', unsafe_allow_html=True)
    if st.button("＝"): on_click("="); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
if st.button("delete"): on_click("delete"); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# --- モード切替 ---
st.write("---")
m_cols = st.columns(4)
modes = ["通常", "科学計算", "巨数", "値数"]
for i, m in enumerate(modes):
    if m_cols[i].button(m, key=f"m_{m}"):
        st.session_state.mode = m; st.rerun()

# --- 巨数モード（ヨクト y から ヨタ Y まで） ---
if st.session_state.mode == "巨数":
    st.write("**巨数単位（数値の後に付けて計算）**")
    draw_row(["Y", "Z", "E", "P", "T"])
    draw_row(["G", "M", "k", "h", "da"])
    draw_row(["d", "c", "m", "μ", "n"])
    draw_row(["p", "f", "a", "z", "y"])
elif st.session_state.mode == "科学計算":
    draw_row(["sin(", "cos(", "tan(", "log(", "exp("])
