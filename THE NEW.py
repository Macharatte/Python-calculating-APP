import streamlit as st
import math
import statistics
import re

# --- ページ設定 ---
st.set_page_config(page_title="Python Calculator", layout="centered")

# --- デバイス別・最適化CSS ---
st.markdown("""
<style>
    /* 1. 全体のスクロールと余白の制限 */
    html, body, [data-testid="stAppViewContainer"] {
        overflow-x: hidden !important;
        width: 100vw;
    }
    header {visibility: hidden;}

    .main .block-container { 
        padding: 1rem 0.5rem !important; 
        max-width: 600px !important;
    }

    /* 2. ボタンの基本デザイン */
    div.stButton > button {
        width: 100% !important; 
        height: 65px !important; /* 高さをしっかり確保 */
        font-size: 20px !important;
        border-radius: 12px !important;
        font-weight: bold !important;
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
        border: 2px solid var(--border-color) !important;
        transition: 0.2s;
    }

    /* 3. スマホでボタンが細くなるのを防ぐためのグリッド設定 */
    /* 画面幅が600px以下の時（スマホ） */
    @media (max-width: 600px) {
        [data-testid="stHorizontalBlock"] {
            display: grid !important;
            grid-template-columns: repeat(3, 1fr) !important; /* スマホは3列にする */
            gap: 8px !important;
        }
        div.stButton > button {
            height: 70px !important; /* スマホではさらに押しやすく大きく */
            font-size: 22px !important;
        }
    }

    /* 4. ディスプレイ表示 */
    .display-container {
        display: flex; align-items: center; justify-content: flex-end;
        font-size: 40px; font-weight: bold;
        margin-bottom: 20px; padding: 15px; 
        border-bottom: 4px solid currentColor;
        min-height: 90px; word-break: break-all;
    }

    /* カラー設定 */
    :root { --bg-color: #000000; --text-color: #ffffff; --border-color: #333333; }
    @media (prefers-color-scheme: dark) {
        :root { --bg-color: #ffffff; --text-color: #000000; --border-color: #dddddd; }
    }

    .delete-btn div.stButton > button {
        background-color: #FF0000 !important; color: white !important;
        height: 70px !important; border: none !important; margin-top: 10px;
    }

    .calc-title { text-align: center; font-size: 32px; font-weight: 800; margin-bottom: 10px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="calc-title">python calculator</div>', unsafe_allow_html=True)

if 'formula' not in st.session_state: st.session_state.formula = ""
if 'mode' not in st.session_state: st.session_state.mode = "通常"
if 'last_was_equal' not in st.session_state: st.session_state.last_was_equal = False

st.markdown(f'<div class="display-container"><span>{st.session_state.formula if st.session_state.formula else "0"}</span></div>', unsafe_allow_html=True)

# --- 計算ロジック ---
def on_click(char):
    current = st.session_state.formula
    operators = ["+", "−", "×", "÷", "^^", ".", "°"]
    if st.session_state.last_was_equal:
        if char in operators: st.session_state.last_was_equal = False
        else: current = ""; st.session_state.formula = ""; st.session_state.last_was_equal = False
    
    if char == "＝":
        if not current: return
        try:
            f = current.replace('×', '*').replace('÷', '/').replace('−', '-')
            f = re.sub(r'([\d\.]+)\°', r'math.radians(\1)', f)
            f = f.replace('√', 'math.sqrt').replace('^^', '**').replace('π', 'math.pi').replace('e', 'math.e')
            f = f.replace('sin', 'math.sin').replace('cos', 'math.cos').replace('tan', 'math.tan').replace('abs', 'abs').replace('log', 'math.log10')
            u_map = {'Q':'1e30','R':'1e27','Y':'1e24','Z':'1e21','E':'1e18','P':'1e15','T':'1e12','G':'1e9','M':'1e6','k':'1e3','h':'1e2','da':'1e1','d':'1e-1','c':'1e-2','m':'1e-3','μ':'1e-6','n':'1e-9','p':'1e-12','f':'1e-15','a':'1e-18','z':'1e-21','y':'1e-24','r':'1e-27','q':'1e-30'}
            for sym, val in u_map.items(): f = re.sub(rf'(\d+){sym}', rf'(\1*{val})', f)
            res = eval(f, {"__builtins__": None}, {"math": math, "statistics": statistics, "abs": abs})
            st.session_state.formula = format(res, '.10g')
            st.session_state.last_was_equal = True
        except: st.session_state.formula = "Error"
    elif char == "delete": st.session_state.formula = ""
    else:
        if not current:
            if char in ["+", "×", "÷", "^^", ".", "°"]: return
            st.session_state.formula += str(char); return
        if current[-1] in operators and char in operators:
            st.session_state.formula = current[:-1] + str(char); return
        st.session_state.formula += str(char)

# --- ボタン配置 ---
# 通常モードのボタン（スマホでは自動で3列に折り返されます）
buttons = ["7", "8", "9", "π", "÷", "+", "4", "5", "6", "e", "√", "−", "1", "2", "3", "i", "^^", "×", "(", ")", "0", "00", ".", "＝"]

cols = st.columns(6) # 内部的には6列で作るが、CSSでスマホ時は3列に強制
for i, b in enumerate(buttons):
    with cols[i % 6]:
        if st.button(b, key=f"btn_{b}"):
            on_click(b); st.rerun()

st.markdown('<div class="delete-btn">', unsafe_allow_html=True)
if st.button("delete", use_container_width=True): on_click("delete"); st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# モード切替
st.write("---")
m_cols = st.columns(4)
modes = ["通常", "科学計算", "巨数", "値数"]
for m_idx, m_name in enumerate(modes):
    if m_cols[m_idx].button(m_name): st.session_state.mode = m_name; st.rerun()

# 各モードの追加ボタン（スマホ3列対応）
if st.session_state.mode != "通常":
    st.write(f"### {st.session_state.mode} モード")
    extra_buttons = []
    if st.session_state.mode == "巨数":
        extra_buttons = ["Q", "R", "Y", "Z", "E", "P", "T", "G", "M", "k", "h", "da", "d", "c", "m", "μ", "n", "p", "f", "a", "z", "y", "r", "q"]
    elif st.session_state.mode == "科学計算":
        extra_buttons = ["sin(", "cos(", "tan(", "°", "abs(", "log(", "(", ")", "e", "π", "√"]
    elif st.session_state.mode == "値数":
        extra_buttons = ["平均([", "中央値([", "最頻値([", "最大([", "最小([", "])"]
    
    e_cols = st.columns(6)
    for i, b in enumerate(extra_buttons):
        with e_cols[i % 6]:
            if st.button(b, key=f"extra_{b}"): on_click(b); st.rerun()
