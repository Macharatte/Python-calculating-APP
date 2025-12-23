import streamlit as st
import math
import statistics
import re
import datetime

# --- ページ設定 ---
st.set_page_config(page_title="Python Calculator", layout="centered")

# --- ボタンの太さを強制固定するCSS ---
st.markdown("""
<style>
    /* 1. 画面全体の余白をゼロにし、横幅を最大化 */
    .main .block-container {
        max-width: 100% !important;
        padding: 5px 2px !important;
    }
    header {visibility: hidden;}
    
    /* 2. 6列を絶対に均等（16.6%）にする設定 */
    [data-testid="stHorizontalBlock"] {
        gap: 2px !important;
        display: flex !important;
        flex-direction: row !important;
        align-items: stretch !important;
        width: 100% !important;
    }
    
    /* ボタンを囲むカラムの幅を強制固定 */
    [data-testid="column"] {
        width: calc(16.66% - 2px) !important;
        min-width: calc(16.66% - 2px) !important;
        flex: 1 1 0% !important;
    }

    /* 3. deleteと＝の行（2列）は50%に固定 */
    .bottom-row [data-testid="column"] {
        width: calc(50% - 2px) !important;
        min-width: calc(50% - 2px) !important;
    }

    /* 4. ボタンの形状（細くなるのを防ぐ） */
    div.stButton > button {
        width: 100% !important;
        height: 65px !important;
        font-size: 22px !important;
        border-radius: 4px !important;
        font-weight: bold !important;
        background-color: var(--bg-color) !important;
        color: var(--text-color) !important;
        border: 2px solid var(--border-color) !important;
        padding: 0 !important;
        display: block !important;
    }

    .display-container {
        display: flex; align-items: center; justify-content: flex-end;
        font-size: 45px; font-weight: bold; margin-bottom: 10px; padding: 10px; 
        border-bottom: 4px solid currentColor; min-height: 85px; word-break: break-all;
    }

    :root { --bg-color: #000000; --text-color: #ffffff; --border-color: #444444; }
    @media (prefers-color-scheme: dark) { :root { --bg-color: #ffffff; --text-color: #000000; --border-color: #cccccc; } }
    
    .del-btn div.stButton > button { background-color: #FF0000 !important; color: white !important; border: none !important; }
    .eq-btn div.stButton > button { background-color: #2e7d32 !important; color: white !important; border: none !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="text-align:center; font-weight:800; font-size:22px; margin-bottom:5px;">PYTHON CALCULATOR</div>', unsafe_allow_html=True)

# --- 状態管理 ---
ss = st.session_state
if 'formula' not in ss: ss.formula = ""
if 'mode' not in ss: ss.mode = "通常"
if 'last_was_equal' not in ss: ss.last_was_equal = False
if 'history' not in ss: ss.history = []

st.markdown(f'<div class="display-container"><span>{ss.formula if ss.formula else "0"}</span></div>', unsafe_allow_html=True)

# --- ロジック ---
def on_click(char):
    operators = ["+", "−", "×", "÷", "^^", ".", "°"]
    if ss.formula == "Error" or ss.last_was_equal:
        if char in operators and ss.formula != "Error": ss.last_was_equal = False
        else: ss.formula = ""; ss.last_was_equal = False
    if char == "＝":
        if not ss.formula: return
        try:
            f = ss.formula.replace('×', '*').replace('÷', '/').replace('−', '-').replace('m', '-')
            res = eval(f, {"math": math, "statistics": statistics, "abs": abs})
            res_str = format(res, '.10g')
            ss.history.insert(0, {"f": ss.formula, "r": res_str, "t": datetime.datetime.now().strftime("%H:%M")})
            ss.formula = res_str; ss.last_was_equal = True
        except: ss.formula = "Error"
    elif char == "delete": ss.formula = ""
    elif char == "(-)":
        if not ss.formula or ss.formula[-1] in ["+", "−", "×", "÷", "(", "^^"]: ss.formula += "−"
        else: on_click("−")
    else:
        if not ss.formula and char in operators: return
        if ss.formula and ss.formula[-1] in operators and char in operators:
            ss.formula = ss.formula[:-1] + str(char); return
        ss.formula += str(char)

# --- メインキーパッド（均等6列） ---
main_btns = [
    "7", "8", "9", "π", "√",  "+",
    "4", "5", "6", "e", "^^", "−",
    "1", "2", "3", "i", "(-)", "×",
    "0", "00", ".", "(", ")", "÷"
]

cols = st.columns(6)
for i, b in enumerate(main_btns):
    with cols[i % 6]:
        if st.button(b, key=f"k{i}"): on_click(b); st.rerun()

# --- 下部ボタン（50/50） ---
st.markdown('<div class="bottom-row">', unsafe_allow_html=True)
bot_c1, bot_c2 = st.columns(2)
with bot_c1:
    st.markdown('<div class="del-btn">', unsafe_allow_html=True)
    if st.button("delete", use_container_width=True, key="btn_del"): on_click("delete"); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
with bot_c2:
    st.markdown('<div class="eq-btn">', unsafe_allow_html=True)
    if st.button("＝", use_container_width=True, key="btn_eq"): on_click("＝"); st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr style="margin:10px 0; opacity:0.1;">', unsafe_allow_html=True)

# --- モード切替 ---
m_cols = st.columns(5)
modes = ["通常", "科学計算", "巨数", "値数", "履歴"]
for i, m in enumerate(modes):
    if m_cols[i].button(m, key=f"m{i}"): ss.mode = m; st.rerun()

# モード別ボタン
if ss.mode != "通常":
    if ss.mode == "履歴":
        for i, item in enumerate(ss.history[:5]):
            if st.button(f"{item['f']} = {item['r']}", key=f"h{i}", use_container_width=True):
                ss.formula = item['r']; ss.mode = "通常"; st.rerun()
    else:
        extra = []
        if ss.mode == "巨数": extra = ["Q", "R", "Y", "Z", "E", "P", "T", "G", "M", "k", "h", "da", "d", "c", "m", "μ", "n", "p", "f", "a", "z", "y", "r", "q"]
        elif ss.mode == "科学計算": extra = ["sin(", "cos(", "tan(", "°", "abs(", "log("]
        elif ss.mode == "値数": extra = ["平均([", "中央値([", "最頻値([", "最大([", "最小([", "])", "偏差値(", "期待値(", ","]
        e_cols = st.columns(6)
        for i, b in enumerate(extra):
            with e_cols[i % 6]:
                if st.button(b, key=f"e{i}"): on_click(b); st.rerun()
