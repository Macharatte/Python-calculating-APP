import streamlit as st
import math
import statistics
import re

# --- ページ設定 ---
st.set_page_config(page_title="Calculator Pro", layout="centered")

# --- スタイル強制適用 ---
st.markdown("""
<style>
    header {visibility: hidden;}
    .main .block-container { padding: 0px !important; max-width: 100% !important; margin: 0px !important; }
    div.stButton > button {
        width: 100% !important; height: 100px !important;
        font-size: 30px !important; font-weight: 900 !important;
        margin: 0px !important; border: 2px solid #000 !important;
        border-radius: 0px !important; background-color: #ffffff !important; color: #000000 !important;
    }
    .wide-btn div.stButton > button { height: 110px !important; font-size: 35px !important; background-color: #eeeeee !important; }
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }
    .display-box { 
        font-size: 50px; font-weight: bold; text-align: right; 
        padding: 30px; background: #000000; color: #00ff00; 
        border-bottom: 5px solid #333333; min-height: 140px; font-family: monospace;
    }
    .calc-title { text-align: center; font-size: 24px; font-weight: bold; padding: 15px; background: #222; color: #fff; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="calc-title">SCIENTIFIC CALCULATOR PRO</div>', unsafe_allow_html=True)

if 'formula' not in st.session_state: st.session_state.formula = ""
if 'mode' not in st.session_state: st.session_state.mode = "通常"

st.markdown(f'<div class="display-box">{st.session_state.formula if st.session_state.formula else "0"}</div>', unsafe_allow_html=True)

def on_click(char):
    if char == "＝":
        try:
            f = st.session_state.formula.replace('×', '*').replace('÷', '/').replace('−', '-')
            f = f.replace('√', 'math.sqrt').replace('^^', '**').replace('π', 'math.pi')
            u_map = {'Y':'1e24','M':'1e6','k':'1e3','m':'1e-3','n':'1e-9'}
            for sym, val in u_map.items(): f = re.sub(rf'(\d+){sym}', rf'(\1*{val})', f)
            res = eval(f, {"__builtins__": None}, {"math": math, "statistics": statistics})
            st.session_state.formula = format(res, '.10g')
        except: st.session_state.formula = "Error"
    elif char == "C": st.session_state.formula = ""
    elif char == "del": st.session_state.formula = st.session_state.formula[:-1]
    else: st.session_state.formula += str(char)

def draw_row(labels):
    cols = st.columns(4)
    for i, l in enumerate(labels):
        if cols[i].button(l, key=f"b_{l}_{i}_{st.session_state.mode}"):
            on_click(l); st.rerun()

draw_row(["7", "8", "9", "÷"])
draw_row(["4", "5", "6", "×"])
draw_row(["1", "2", "3", "−"])
draw_row(["0", ".", "C", "+"])
draw_row(["(", ")", "00", "π"])

st.markdown('<div class="wide-btn">', unsafe_allow_html=True)
c1, c2 = st.columns(2)
if c1.button("＝", key="eq"): on_click("＝"); st.rerun()
if c2.button("DEL", key="dl"): on_click("del"); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
m_cols = st.columns(4)
for i, m in enumerate(["通常", "科学計算", "巨数", "値数"]):
    if m_cols[i].button(m, key=f"m_{m}"): st.session_state.mode = m; st.rerun()

if st.session_state.mode == "巨数":
    draw_row(["y", "z", "a", "f"])
    draw_row(["p", "n", "μ", "m"])
