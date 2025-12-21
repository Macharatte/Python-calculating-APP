import streamlit as st
import math
import statistics
import re

# --- ページ設定とスタイル強制上書き ---
st.set_page_config(page_title="Calculator Pro", layout="centered")

# CSSを極限まで強力にしました。これでも変わらない場合はブラウザのキャッシュクリアが必要です。
st.markdown("""
<style>
    /* 左右の巨大な空白を消す */
    header {visibility: hidden;}
    .main .block-container {
        padding: 0px !important; 
        max-width: 100% !important;
        margin: 0px !important;
    }
    
    /* ボタンを強制的に太く、大きく、隙間なくする */
    .stButton > button {
        width: 100% !important;
        height: 100px !important; /* 1:1に近づけるためさらに高く */
        font-size: 32px !important; /* 文字を極太に */
        font-weight: 900 !important;
        margin: 0px !important;
        padding: 0px !important;
        border: 2px solid #000000 !important; /* 枠線を黒く太く */
        border-radius: 0px !important;
        background-color: #ffffff !important;
        color: #000000 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }

    /* ＝ と DELETE をさらに巨大化 */
    .wide-btn .stButton > button {
        height: 120px !important;
        font-size: 40px !important;
        background-color: #333333 !important;
        color: #ffffff !important;
    }

    /* カラムの隙間を排除 */
    [data-testid="column"] { padding: 0px !important; margin: 0px !important; }
    [data-testid="stHorizontalBlock"] { gap: 0px !important; }

    /* ディスプレイを画面上部に固定 */
    .display-box { 
        font-size: 60px; font-weight: bold; text-align: right; 
        padding: 30px; background: #000000; color: #00ff00; 
        border-bottom: 5px solid #444; min-height: 150px;
        font-family: 'Courier New', monospace;
    }
    .calc-title {
        text-align: center; font-size: 24px; font-weight: bold;
        padding: 10px; background: #1a1a1a; color: white;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="calc-title">SCIENTIFIC CALCULATOR PRO</div>', unsafe_allow_html=True)

if 'formula' not in st.session_state: st.session_state.formula = ""
if 'mode' not in st.session_state: st.session_state.mode = "通常"

st.markdown(f'<div class="display-box">{st.session_state.formula if st.session_state.formula else "0"}</div>', unsafe_allow_html=True)

# --- ロジック ---
def on_click(char):
    if char == "＝":
        if not st.session_state.formula: return
        try:
            f = st.session_state.formula.replace('×', '*').replace('÷', '/').replace('−', '-')
            f = f.replace('√', 'math.sqrt').replace('^^', '**').replace('10^', '10**').replace('π', 'math.pi')
            u_map = {'Y':'1e24','Z':'1e21','E':'1e18','P':'1e15','T':'1e12','G':'1e9','M':'1e6','k':'1e3','m':'1e-3','μ':'1e-6','n':'1e-9'}
            for sym, val in u_map.items(): f = re.sub(rf'(\d+){sym}', rf'(\1*{val})', f)
            context = {"math": math, "statistics": statistics}
            result = eval(f, {"__builtins__": None}, context)
            st.session_state.formula = format(result, '.10g')
        except: st.session_state.formula = "Error"
    elif char == "C": st.session_state.formula = ""
    elif char == "del": st.session_state.formula = st.session_state.formula[:-1]
    else: st.session_state.formula += str(char)

# --- 4列配置（1つ1つを巨大にするため列数を減らしました） ---
# これにより、一つ一つのボタンが横に広がり、＋ボタンも確実に見えるようになります。
def draw_row(labels):
    cols = st.columns(4)
    for i, label in enumerate(labels):
        if cols[i].button(label, key=f"btn_{label}_{i}"):
            on_click(label); st.rerun()

draw_row(["7", "8", "9", "÷"])
draw_row(["4", "5", "6", "×"])
draw_row(["1", "2", "3", "−"])
draw_row(["0", ".", "C", "+"]) # + をここ（右下）に配置しました
draw_row(["(", ")", "00", "π"])

# ＝ と DELETE
st.markdown('<div class="wide-btn">', unsafe_allow_html=True)
c1, c2 = st.columns(2)
if c1.button("＝", key="eq"): on_click("＝"); st.rerun()
if c2.button("DEL", key="del"): on_click("del"); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

st.write("---")
m_cols = st.columns(4)
for i, m in enumerate(["通常", "科学計算", "巨数", "値数"]):
    if m_cols[i].button(m, key=f"m_{m}"): st.session_state.mode = m; st.rerun()

if st.session_state.mode == "科学計算":
    draw_row(["sin(", "cos(", "tan(", "log("])
elif st.session_state.mode == "巨数":
    draw_row(["n", "μ", "m", "k"])
    draw_row(["M", "G", "T", "P"])
